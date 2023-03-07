#!/usr/bin/env python
"""
Main entry point for a click based CLI.
"""
import functools
import logging

import click
from firestone_lib import cli
from firestone_lib import utils as firestone_utils

from addressbook.client import api_client
from addressbook.client import configuration
from addressbook.client import exceptions
from addressbook.client.api import addressbook_api
from addressbook.client.models import addressbook as addressbook_model

_LOGGER = logging.getLogger(__name__)


def api_exc(func):
    """Handle ApiExceptions in all functions."""

    async def wrapper(*args, **kwargs):
        api_obj = args[0]["api_obj"]
        resp = None
        try:
            resp = await func(*args, **kwargs)
        except exceptions.ApiException as apie:
            click.echo(apie.reason)
            await api_obj.api_client.close()
        return resp

    return functools.update_wrapper(wrapper, func)


@click.group()
@click.option("--debug", help="Turn on debugging", is_flag=True)
@click.option(
    "--api-key",
    help="The API key to authorize against API",
    envvar="API_KEY",
)
@click.option(
    "--api-url",
    help="The URL to the API",
    required=True,
    envvar="API_URL",
)
@click.option("--threads", help="The number of threads for client side", type=int, default=1)
@click.pass_context
def main(ctx, debug, api_key, api_url, threads):
    """Addressbook resource

    A simple addressbook example
    """
    try:
        cli.init_logging("addressbook.resources.logging", "cli.conf")
    # pylint: disable=broad-except
    except Exception:
        logging.basicConfig(
            level=logging.INFO,
            format="# %(asctime)s - [%(threadName)s] %(name)s:%(lineno)d %(levelname)s - %(message)s",
        )

    logging.getLogger("asyncio").setLevel(logging.CRITICAL)
    if debug:
        _LOGGER.setLevel(logging.DEBUG)
        logging.getLogger().setLevel(logging.DEBUG)
        logging.getLogger("addressbook").setLevel(logging.DEBUG)
        logging.getLogger("aiohttp").setLevel(logging.DEBUG)
        logging.getLogger("urllib3").setLevel(logging.DEBUG)
        logging.getLogger("httplib").setLevel(logging.DEBUG)

    config = configuration.Configuration(host=api_url)
    config.debug = debug
    if api_key:
        config.access_token = api_key
    aclient = api_client.ApiClient(configuration=config, pool_threads=threads)

    ctx.obj = {
        "api_client": aclient,
    }
    _LOGGER.debug(f"ctx.obj: {ctx.obj}")


@main.group()
@click.pass_obj
def addressbook(ctx_obj):
    """High level command for an addressbook."""
    _LOGGER.debug(f"ctx_obj: {ctx_obj}")
    ctx_obj["api_obj"] = addressbook_api.AddressbookApi(api_client=ctx_obj["api_client"])


@addressbook.command("list")
@click.option("--city", help="Filter by city name", type=str, required=False)
@click.option("--limit", help="Limit the number of responses back", type=int, required=False)
@click.option("--offset", help="The offset to start returning resources", type=int, required=False)
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


@addressbook.command("create")
@click.option(
    "--person",
    help="This is a person object that lives at this address.",
    type=cli.FromJSON(),
    required=False,
)
@click.option("--addrtype", help="The address type, e.g. work or home", type=str, required=True)
@click.option(
    "--street", help="The street and civic number of this address", type=str, required=True
)
@click.option("--city", help="The city of this address", type=str, required=True)
@click.option("--state", help="The state of this address", type=str, required=True)
@click.option("--country", help="The country of this address", type=str, required=True)
@click.pass_obj
@firestone_utils.click_coro
@api_exc
async def addressbook_post(ctx_obj, person, addrtype, street, city, state, country):
    """Create a new address in this addressbook, a new address key will be created."""
    api_obj = ctx_obj["api_obj"]
    params = {
        "person": person,
        "addrtype": addrtype,
        "street": street,
        "city": city,
        "state": state,
        "country": country,
    }

    req_body = addressbook_model.Addressbook()
    req_body.from_dict(params)
    resp = await api_obj.addressbook_post(req_body)
    _LOGGER.debug(f"resp: {resp}")


@addressbook.command("delete")
@click.argument("address_key", type=str)
@click.pass_obj
@firestone_utils.click_coro
@api_exc
async def addressbook_address_key_delete(ctx_obj, address_key):
    """Delete an address from this addressbook."""
    api_obj = ctx_obj["api_obj"]
    params = {
        "address_key": address_key,
    }

    resp = await api_obj.addressbook_address_key_delete(**params)
    _LOGGER.debug(f"resp: {resp}")


@addressbook.command("get")
@click.option("--city", help="Filter by city name", type=str, required=False)
@click.argument("address_key", type=str)
@click.pass_obj
@firestone_utils.click_coro
@api_exc
async def addressbook_address_key_get(ctx_obj, city, address_key):
    """Get a specific address from this addressbook."""
    api_obj = ctx_obj["api_obj"]
    params = {
        "city": city,
        "address_key": address_key,
    }

    resp = await api_obj.addressbook_address_key_get(**params)
    _LOGGER.debug(f"resp: {resp}")


@addressbook.command("update")
@click.option(
    "--person",
    help="This is a person object that lives at this address.",
    type=cli.FromJSON(),
    required=False,
)
@click.option("--addrtype", help="The address type, e.g. work or home", type=str, required=True)
@click.option(
    "--street", help="The street and civic number of this address", type=str, required=True
)
@click.option("--city", help="The city of this address", type=str, required=True)
@click.option("--state", help="The state of this address", type=str, required=True)
@click.option("--country", help="The country of this address", type=str, required=True)
@click.pass_obj
@firestone_utils.click_coro
@api_exc
async def addressbook_address_key_put(ctx_obj, person, addrtype, street, city, state, country):
    """Put a new address in this addressbook, with the given address key."""
    api_obj = ctx_obj["api_obj"]
    params = {
        "person": person,
        "addrtype": addrtype,
        "street": street,
        "city": city,
        "state": state,
        "country": country,
    }

    resp = await api_obj.addressbook_address_key_put(**params)
    _LOGGER.debug(f"resp: {resp}")


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    main()