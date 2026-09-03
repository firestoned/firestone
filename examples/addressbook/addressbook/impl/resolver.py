# coding: utf-8
"""
The one piece of validation you write by hand.

Firestone works out *what* every rule needs; this works out *how* to fetch it.
Swap the dictionaries below for your database, ORM or cache and nothing else
about the generated validation package changes.

Every lookup a single request needs arrives in one call, already de-duplicated,
so a request that trips ten rules still costs one round trip.
"""

import collections
import logging

from fastapi.responses import JSONResponse

from addressbook.validation import RefRequest
from addressbook.validation import ValidationError

_LOGGER = logging.getLogger(__name__)

# Stand-ins for the tables a real service would query.
PERSONS = {
    "foo": {"first_name": "foo", "last_name": "bar", "uuid": "3fa8-4f66"},
}
ADDRESSBOOK = {
    "foo": {"address_key": "bar", "city": "foo", "person": {"first_name": "foo"}},
}

# A rule's 'key' is a path into the resource being looked up, not a column name.
# 'person.first_name' means "the addressbook entry whose person's first_name is
# this", which each backend expresses differently, so the mapping from a logical
# path to a storage predicate belongs here, written out once per backend.
LOOKUPS = {
    ("persons", "first_name"): PERSONS,
    ("addressbook", "person.first_name"): ADDRESSBOOK,
}


class InMemoryResolver:
    """Resolves the lookups the generated rules ask for.

    A real implementation groups the requests the same way and issues one query
    per (kind, key), translating the key into whatever that backend needs: a
    column for a scalar, a JSON path expression in Postgres, a dotted field in
    Mongo, a secondary index in Redis.
    """

    async def resolve(self, requests: list, ctx) -> dict:
        """Resolve every lookup for one request.

        :param list requests: the :class:`RefRequest` objects the rules need
        :param ctx: the read-only request context, for anything a lookup has to be
            scoped by. This example needs none of it; a multi-tenant service would
            take the tenant from here rather than trusting the request body.
        :return: a mapping of request id to the resource found, missing ones left out
        :rtype: dict
        """
        del ctx

        by_lookup = collections.defaultdict(list)
        for request in requests:
            by_lookup[(request.kind, request.key)].append(request)

        found = {}
        for lookup, group in by_lookup.items():
            values = [request.value for request in group]
            _LOGGER.debug(f"Looking up {len(values)} {lookup[0]} by {lookup[1]}: {values}")
            for request in group:
                resource = self.lookup(request)
                if resource is not None:
                    found[request.id] = resource

        return found

    def lookup(self, request: RefRequest):
        """Find a single resource, or None if there is no such thing.

        :param RefRequest request: the kind to look in, the path to match on and
            the value to match
        """
        table = LOOKUPS.get((request.kind, request.key))
        if table is None:
            raise NotImplementedError(
                f"Nothing knows how to look up {request.kind} by {request.key}"
            )

        return table.get(request.value)


def problem_response(error: ValidationError) -> JSONResponse:
    """Render a validation failure as the response the OpenAPI spec advertises.

    RFC 9457 puts the problem at the top level of the body and serves it as
    application/problem+json, so this cannot go through ``HTTPException``: that
    wraps whatever you give it in a ``detail`` key and sends application/json.

    Registering an exception handler for :class:`ValidationError` on the app does
    the same thing for every route at once, which is what you would do for real.
    """
    return JSONResponse(
        status_code=error.status,
        content=error.to_problem(),
        media_type="application/problem+json",
    )
