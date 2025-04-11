#!/usr/bin/env python
"""
Firestone CLI module for persons
"""
import functools
import json
import logging
import os
import sys

import click
from firestone_lib import cli
from firestone_lib import utils as firestone_utils

from addressbook.client import api_client
from addressbook.client import configuration
from addressbook.client import exceptions


from addressbook.client.api import persons_api
from addressbook.client.models import person as person_model
from addressbook.client.models import create_person as create_person_model
from addressbook.client.models import update_person as update_person_model

_LOGGER = logging.getLogger(__name__)


def api_exc(func):
    """Handle ApiExceptions in all functions."""

    async def wrapper(*args, **kwargs):
        resp = None
        try:
            return await func(*args, **kwargs)
        except exceptions.ApiException as apie:
            if apie.body:
                click.echo(apie.body)
            else:
                click.echo(apie.reason)

            api_obj = args[0].get("api_obj")
            if api_obj:
                await api_obj.api_client.close()
        sys.exit(-1)

    return functools.update_wrapper(wrapper, func)


def init():
    """Initialize persons resource CLI."""

    @click.group()
    @firestone_utils.click_coro
    @click.pass_obj
    async def persons(ctx_obj):
        """High level command for an persons."""
        _LOGGER.debug(f"ctx_obj: {ctx_obj}")
        config = ctx_obj["api_client_config"]
        aclient = api_client.ApiClient(configuration=config)
        ctx_obj["api_obj"] = persons_api.PersonsApi(api_client=aclient)

    # pylint: disable=redefined-builtin
    @persons.command("create")
    @click.option("--age", help="The person's age", type=int, show_default=True, required=False)
    @click.option(
        "--first-name", help="The person's first name", type=str, show_default=True, required=False
    )
    @click.option(
        "--hobbies",
        help="The person's hobbies",
        type=cli.StrList,
        show_default=True,
        required=False,
    )
    @click.option(
        "--last-name", help="The person's last name", type=str, show_default=True, required=False
    )
    @click.option(
        "--uuid",
        help="A UUID associated to this person",
        type=str,
        show_default=True,
        required=False,
    )
    @click.pass_obj
    @firestone_utils.click_coro
    @api_exc
    async def persons_post(ctx_obj, age, first_name, hobbies, last_name, uuid):
        """Create a new person in this collection, a new UUID key will be created"""
        api_obj = ctx_obj["api_obj"]
        params = {
            "age": age,
            "first_name": first_name,
            "hobbies": hobbies,
            "last_name": last_name,
            "uuid": uuid,
        }
        req_body = create_person_model.CreatePerson(**params)
        resp = await api_obj.persons_post(req_body)
        _LOGGER.debug(f"resp: {resp}")

        if isinstance(resp, list):
            click.echo(json.dumps([obj.to_dict() for obj in resp]))
            return

        if resp:
            click.echo(json.dumps(resp.to_dict()))
            return

        click.echo("No data returned")

    @persons.command("list")
    @click.option(
        "--last-name", help="Filter by last name", type=str, show_default=True, required=False
    )
    @click.option(
        "--limit",
        help="Limit the number of responses back",
        type=int,
        show_default=True,
        required=False,
    )
    @click.option(
        "--offset",
        help="The offset to start returning resources",
        type=int,
        show_default=True,
        required=False,
    )
    @click.pass_obj
    @firestone_utils.click_coro
    @api_exc
    async def persons_get(ctx_obj, last_name, limit, offset):
        """List all persons in this collection"""
        api_obj = ctx_obj["api_obj"]
        params = {
            "last_name": last_name,
            "limit": limit,
            "offset": offset,
        }

        resp = await api_obj.persons_get(**params)
        _LOGGER.debug(f"resp: {resp}")

        if isinstance(resp, list):
            click.echo(json.dumps([obj.to_dict() for obj in resp]))
            return

        if resp:
            click.echo(json.dumps(resp.to_dict()))
            return

        click.echo("No data returned")

    @persons.command("delete")
    @click.argument("uuid", type=str)
    @click.pass_obj
    @firestone_utils.click_coro
    @api_exc
    async def persons_uuid_delete(ctx_obj, uuid):
        """Delete operation for persons"""
        api_obj = ctx_obj["api_obj"]
        params = {}

        resp = await api_obj.persons_uuid_delete(uuid, **params)
        _LOGGER.debug(f"resp: {resp}")

        if isinstance(resp, list):
            print(json.dumps([obj.to_dict() for obj in resp]))
            return

        print(json.dumps(resp.to_dict()) if resp else "None")

    @persons.command("get")
    @click.option("--last-name", help="Filter by last name", type=str, required=False)
    @click.argument("uuid", type=str)
    @click.pass_obj
    @firestone_utils.click_coro
    @api_exc
    async def persons_uuid_get(ctx_obj, last_name, uuid):
        """Get a specific person from this collection"""
        api_obj = ctx_obj["api_obj"]
        params = {
            "last_name": last_name,
        }

        resp = await api_obj.persons_uuid_get(uuid, **params)
        _LOGGER.debug(f"resp: {resp}")

        if isinstance(resp, list):
            print(json.dumps([obj.to_dict() for obj in resp]))
            return

        print(json.dumps(resp.to_dict()) if resp else "None")

    @persons.command("update")
    @click.option("--age", help="The person's age", type=int, required=False)
    @click.option("--first-name", help="The person's first name", type=str, required=False)
    @click.option("--hobbies", help="The person's hobbies", type=cli.StrList, required=False)
    @click.option("--last-name", help="The person's last name", type=str, required=False)
    @click.argument("uuid", type=str)
    @click.argument("uuid", type=str)
    @click.pass_obj
    @firestone_utils.click_coro
    @api_exc
    async def persons_uuid_put(ctx_obj, age, first_name, hobbies, last_name, uuid, uuid):
        """Put a new person in this collection, with the given UUId key"""
        api_obj = ctx_obj["api_obj"]
        params = {
            "age": age,
            "first_name": first_name,
            "hobbies": hobbies,
            "last_name": last_name,
        }

        req_body = update_person_model.UpdatePerson(**params)
        resp = await api_obj.persons_uuid_put(uuid, uuid, req_body)
        _LOGGER.debug(f"resp: {resp}")

        if isinstance(resp, list):
            print(json.dumps([obj.to_dict() for obj in resp]))
            return

        print(json.dumps(resp.to_dict()) if resp else "None")

    return persons
