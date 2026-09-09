# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from addressbook.apis.addressbook_api_base import BaseAddressbookApi
import addressbook.impl

from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    HTTPException,
    Path,
    Query,
    Response,
    Security,
    status,
)

from addressbook.models.extra_models import TokenModel  # noqa: F401
from pydantic import Field, StrictBool, StrictInt, StrictStr, field_validator
from typing import Any, List, Optional
from typing_extensions import Annotated
from addressbook.models.addressbook import Addressbook
from addressbook.models.create_addressbook import CreateAddressbook
from addressbook.models.update_addressbook import UpdateAddressbook
from addressbook.security_api import get_token_bearer_auth
from addressbook.impl.resolver import InMemoryResolver, problem_response
from addressbook.validation import ValidationError, validate


class AddressBook(BaseAddressbookApi):

    async def addressbook_get(
        self,
        city: Annotated[Optional[StrictStr], Field(description="Filter by city name")] = Query(
            None, description="Filter by city name", alias="city"
        ),
        limit: Annotated[
            Optional[StrictInt], Field(description="Limit the number of responses back")
        ] = Query(None, description="Limit the number of responses back", alias="limit"),
        offset: Annotated[
            Optional[StrictInt], Field(description="The offset to start returning resources")
        ] = Query(None, description="The offset to start returning resources", alias="offset"),
    ) -> List[Addressbook]:
        """List all addresses in this addressbook."""
        return [
            {
                "address_key": "bar",
                "addrtype": "home",
                "street": "400 foobar road",
                "city": "foo",
                "country": "ca",
                "state": "ca",
                "is_valid": True,
                "person": {
                    "first_name": "foo",
                    "last_name": "bar",
                },
            },
            {
                "address_key": "foo",
                "addrtype": "home",
                "street": "500 foobar road",
                "city": "foo",
                "country": "ca",
                "state": "ca",
                "is_valid": False,
                "person": {
                    "first_name": "bar",
                    "last_name": "foo",
                },
            },
        ]

    async def addressbook_post(
        self,
        create_addressbook: Annotated[
            CreateAddressbook, Field(description="The request body for /addressbook")
        ] = Body(None, description="The request body for /addressbook"),
        limit: Annotated[
            Optional[StrictInt], Field(description="Limit the number of responses back")
        ] = Query(None, description="Limit the number of responses back", alias="limit"),
        offset: Annotated[
            Optional[StrictInt], Field(description="The offset to start returning resources")
        ] = Query(None, description="The offset to start returning resources", alias="offset"),
    ) -> CreateAddressbook:
        """Create a new address in this addressbook, a new address key will be created."""
        print(f"create_addressbook: {create_addressbook}")

        # Everything declared in addressbook.yaml runs here, in one call. For this
        # resource that is the 'person' reference: an address can only be created
        # for a person who already exists.
        try:
            await validate("post", "addressbook", create_addressbook, resolver=InMemoryResolver())
        except ValidationError as exc:
            # Returned, not raised: RFC 9457 wants the problem at the top level of
            # the body, and HTTPException would nest it under 'detail'.
            return problem_response(exc)

        return create_addressbook.to_dict()
