#!/usr/bin/env python
"""
Firestone CLI module for addressbook
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


from addressbook.client.api import addressbook_api
from addressbook.client.models import addressbook as addressbook_model
from addressbook.client.models import create_addressbook as create_addressbook_model
from addressbook.client.models import update_addressbook as update_addressbook_model

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
    """Initialize addressbook resource CLI."""

    @click.group()
    @firestone_utils.click_coro
    @click.pass_obj
    async def addressbook(ctx_obj):
        """High level command for an addressbook."""
        _LOGGER.debug(f"ctx_obj: {ctx_obj}")
        config = ctx_obj["api_client_config"]
        aclient = api_client.ApiClient(configuration=config)
        ctx_obj["api_obj"] = addressbook_api.AddressbookApi(api_client=aclient)

    # pylint: disable=redefined-builtin
    @addressbook.command("create")
    @click.option(
        "--address-key",
        help="A unique identifier for an addressbook entry.",
        type=str,
        show_default=True,
        required=False,
    )
    @click.option(
        "--addrtype",
        help="The address type, e.g. work or home",
        type=click.Choice(["work", "home"]),
        show_default=True,
        required=True,
    )
    @click.option(
        "--city", help="The city of this address", type=str, show_default=True, required=True
    )
    @click.option(
        "--country", help="The country of this address", type=str, show_default=True, required=True
    )
    @click.option(
        "--is-valid/--no-is-valid",
        help="Address is valid or not",
        is_flag=True,
        show_default=True,
        required=False,
    )
    @click.option(
        "--people",
        help="A list of people's names living there",
        type=cli.StrList,
        show_default=True,
        required=False,
    )
    @click.option(
        "--person",
        help="This is a person object that lives at this address.",
        type=cli.FromJsonOrYaml(),
        show_default=True,
        required=False,
    )
    @click.option(
        "--state", help="The state of this address", type=str, show_default=True, required=True
    )
    @click.option(
        "--street",
        help="The street and civic number of this address",
        type=str,
        show_default=True,
        required=True,
    )
    @click.pass_obj
    @firestone_utils.click_coro
    @api_exc
    async def addressbook_post(
        ctx_obj, address_key, addrtype, city, country, is_valid, people, person, state, street
    ):
        """Create a new address in this addressbook, a new address key will be created."""
        api_obj = ctx_obj["api_obj"]
        params = {
            "address_key": address_key,
            "addrtype": addrtype,
            "city": city,
            "country": country,
            "is_valid": is_valid,
            "people": people,
            "person": person,
            "state": state,
            "street": street,
        }
        req_body = create_addressbook_model.CreateAddressbook(**params)
        resp = await api_obj.addressbook_post(req_body)
        _LOGGER.debug(f"resp: {resp}")

        if isinstance(resp, list):
            click.echo(json.dumps([obj.to_dict() for obj in resp]))
            return

        if resp:
            click.echo(json.dumps(resp.to_dict()))
            return

        click.echo("No data returned")

    @addressbook.command("list")
    @click.option("--city", help="Filter by city name", type=str, show_default=True, required=False)
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
    async def addressbook_get(ctx_obj, city, limit, offset):
        """List all addresses in this addressbook."""
        api_obj = ctx_obj["api_obj"]
        params = {
            "city": city,
            "limit": limit,
            "offset": offset,
        }

        resp = await api_obj.addressbook_get(**params)
        _LOGGER.debug(f"resp: {resp}")

        if isinstance(resp, list):
            click.echo(json.dumps([obj.to_dict() for obj in resp]))
            return

        if resp:
            click.echo(json.dumps(resp.to_dict()))
            return

        click.echo("No data returned")

    @addressbook.command("delete")
    @click.argument("address_key", type=str)
    @click.pass_obj
    @firestone_utils.click_coro
    @api_exc
    async def addressbook_address_key_delete(ctx_obj, address_key):
        """Delete an address from this addressbook."""
        api_obj = ctx_obj["api_obj"]
        params = {}

        resp = await api_obj.addressbook_address_key_delete(address_key, **params)
        _LOGGER.debug(f"resp: {resp}")

        if isinstance(resp, list):
            print(json.dumps([obj.to_dict() for obj in resp]))
            return

        print(json.dumps(resp.to_dict()) if resp else "None")

    @addressbook.command("get")
    @click.argument("address_key", type=str)
    @click.option("--city", help="Filter by city name", type=str, required=False)
    @click.pass_obj
    @firestone_utils.click_coro
    @api_exc
    async def addressbook_address_key_get(ctx_obj, address_key, city):
        """Get a specific address from this addressbook."""
        api_obj = ctx_obj["api_obj"]
        params = {
            "city": city,
        }

        resp = await api_obj.addressbook_address_key_get(address_key, **params)
        _LOGGER.debug(f"resp: {resp}")

        if isinstance(resp, list):
            print(json.dumps([obj.to_dict() for obj in resp]))
            return

        print(json.dumps(resp.to_dict()) if resp else "None")

    @addressbook.command("update")
    @click.argument("address_key", type=str)
    @click.argument("address_key", type=str)
    @click.option(
        "--addrtype",
        help="The address type, e.g. work or home",
        type=click.Choice(["work", "home"]),
        required=False,
    )
    @click.option("--city", help="The city of this address", type=str, required=False)
    @click.option("--country", help="The country of this address", type=str, required=False)
    @click.option("--is-valid", help="Address is valid or not", type=bool, required=False)
    @click.option(
        "--people", help="A list of people's names living there", type=cli.StrList, required=False
    )
    @click.option(
        "--person",
        help="This is a person object that lives at this address.",
        type=cli.FromJsonOrYaml(),
        required=False,
    )
    @click.option("--state", help="The state of this address", type=str, required=False)
    @click.option(
        "--street", help="The street and civic number of this address", type=str, required=False
    )
    @click.pass_obj
    @firestone_utils.click_coro
    @api_exc
    async def addressbook_address_key_put(
        ctx_obj,
        address_key,
        address_key,
        addrtype,
        city,
        country,
        is_valid,
        people,
        person,
        state,
        street,
    ):
        """Update an existing address in this addressbook, with the given address key."""
        api_obj = ctx_obj["api_obj"]
        params = {
            "addrtype": addrtype,
            "city": city,
            "country": country,
            "is_valid": is_valid,
            "people": people,
            "person": person,
            "state": state,
            "street": street,
        }

        req_body = update_addressbook_model.UpdateAddressbook(**params)
        resp = await api_obj.addressbook_address_key_put(address_key, address_key, req_body)
        _LOGGER.debug(f"resp: {resp}")

        if isinstance(resp, list):
            print(json.dumps([obj.to_dict() for obj in resp]))
            return

        print(json.dumps(resp.to_dict()) if resp else "None")

    return addressbook
