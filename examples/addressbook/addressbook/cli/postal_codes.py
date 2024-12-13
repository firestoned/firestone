#!/usr/bin/env python
"""
Firestone CLI module for postal_codes
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


from addressbook.client.api import postal_codes_api
from addressbook.client.models import postal_code as postal_code_model
from addressbook.client.models import create_postal_code as create_postal_code_model

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
    """Initialize postal_codes resource CLI."""

    @click.group()
    @firestone_utils.click_coro
    @click.pass_obj
    async def postal_codes(ctx_obj):
        """High level command for an postal_codes."""
        _LOGGER.debug(f"ctx_obj: {ctx_obj}")
        config = ctx_obj["api_client_config"]
        aclient = api_client.ApiClient(configuration=config)
        ctx_obj["api_obj"] = postal_codes_api.PostalCodesApi(api_client=aclient)

    # pylint: disable=redefined-builtin
    @postal_codes.command("create")
    @click.option(
        "--name", help="The postal code's name/id", type=str, show_default=True, required=False
    )
    @click.pass_obj
    @firestone_utils.click_coro
    @api_exc
    async def postal_codes_post(ctx_obj, name):
        """Create a new postal code in this collection, a new UUID key will be created"""
        api_obj = ctx_obj["api_obj"]
        params = {
            "name": name,
        }
        req_body = create_postal_code_model.CreatePostalCode(**params)
        resp = await api_obj.postal_codes_post(req_body)
        _LOGGER.debug(f"resp: {resp}")

        if isinstance(resp, list):
            click.echo(json.dumps([obj.to_dict() for obj in resp]))
            return

        if resp:
            click.echo(json.dumps(resp.to_dict()))
            return

        click.echo("No data returned")

    @postal_codes.command("list")
    @click.option(
        "--limit",
        help="Limit the number of responses back",
        type=int,
        show_default=True,
        required=False,
    )
    @click.option("--name", help="Filter by name", type=str, show_default=True, required=False)
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
    async def postal_codes_get(ctx_obj, limit, name, offset):
        """List all postal codes in this collection"""
        api_obj = ctx_obj["api_obj"]
        params = {
            "limit": limit,
            "name": name,
            "offset": offset,
        }

        resp = await api_obj.postal_codes_get(**params)
        _LOGGER.debug(f"resp: {resp}")

        if isinstance(resp, list):
            click.echo(json.dumps([obj.to_dict() for obj in resp]))
            return

        if resp:
            click.echo(json.dumps(resp.to_dict()))
            return

        click.echo("No data returned")

    @postal_codes.command("delete")
    @click.argument("uuid", type=str)
    @click.pass_obj
    @firestone_utils.click_coro
    @api_exc
    async def postal_codes_uuid_delete(ctx_obj, uuid):
        """Delete operation for postal_codes"""
        api_obj = ctx_obj["api_obj"]
        params = {}

        resp = await api_obj.postal_codes_uuid_delete(uuid, **params)
        _LOGGER.debug(f"resp: {resp}")

        if isinstance(resp, list):
            print(json.dumps([obj.to_dict() for obj in resp]))
            return

        print(json.dumps(resp.to_dict()) if resp else "None")

    @postal_codes.command("get")
    @click.option("--name", help="Filter by name", type=str, required=False)
    @click.argument("uuid", type=str)
    @click.pass_obj
    @firestone_utils.click_coro
    @api_exc
    async def postal_codes_uuid_get(ctx_obj, name, uuid):
        """Get a specific postal code from this collection"""
        api_obj = ctx_obj["api_obj"]
        params = {
            "name": name,
        }

        resp = await api_obj.postal_codes_uuid_get(uuid, **params)
        _LOGGER.debug(f"resp: {resp}")

        if isinstance(resp, list):
            print(json.dumps([obj.to_dict() for obj in resp]))
            return

        print(json.dumps(resp.to_dict()) if resp else "None")

    return postal_codes
