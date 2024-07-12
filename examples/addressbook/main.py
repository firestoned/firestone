#!/usr/bin/env python
"""
Main entry point for a click based CLI.
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

from addressbook.client.api import persons_api
from addressbook.client.models import person as person_model
from addressbook.client.models import create_person as create_person_model
from addressbook.client.models import update_person as update_person_model

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


@click.group()
@click.option("--debug", help="Turn on debugging", is_flag=True)
@click.option(
    "--api-key",
    help="The API key to authorize against API",
    envvar="API_KEY",
)
@click.option(
    "--api-url",
    help="The API url, e.g. https://localhost",
    envvar="API_URL",
)
@click.option(
    "--client-cert",
    help="Path to the client cert for mutual TLS",
    envvar="CLIENT_CERT",
)
@click.option(
    "--client-key",
    help="Path to the client key for mutual TLS",
    envvar="CLIENT_KEY",
)
@click.option("--trust-proxy", help="Trust the proxy env vars", is_flag=True, default=False)
@click.pass_context
def main(ctx, debug, api_key, api_url, client_cert, client_key, trust_proxy):
    """Addressbook CLI

    This is the CLI for the example Addressbook
    """
    if not trust_proxy:
        for prefix in ["http", "https", "all_http", "all_https"]:
            env_var = f"{prefix}_proxy"
            if env_var in os.environ:
                del os.environ[env_var]
            if env_var.upper() in os.environ:
                del os.environ[env_var.upper()]

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
    if client_cert:
        config.cert_file = client_cert
    if client_key:
        config.key_file = client_key
    if "SSL_CA_CERT" in os.environ:
        config.ssl_ca_cert = os.environ["SSL_CA_CERT"]
    if "REQUESTS_CA_BUNDLE" in os.environ:
        config.ssl_ca_cert = os.environ["REQUESTS_CA_BUNDLE"]

    aclient = api_client.ApiClient(configuration=config)

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


# pylint: disable=redefined-builtin
@addressbook.command("create")
@click.option(
    "--addrtype",
    help="The address type, e.g. work or home",
    type=click.Choice(["work", "home"]),
    required=True,
)
@click.option("--city", help="The city of this address", type=str, required=True)
@click.option("--country", help="The country of this address", type=str, required=True)
@click.option(
    "--people", help="A list of people's names living there", type=cli.StrList, required=False
)
@click.option(
    "--person",
    help="This is a person object that lives at this address.",
    type=cli.FromJsonOrYaml(),
    required=False,
)
@click.option("--state", help="The state of this address", type=str, required=True)
@click.option(
    "--street", help="The street and civic number of this address", type=str, required=True
)
@click.pass_obj
@firestone_utils.click_coro
@api_exc
async def addressbook_post(ctx_obj, addrtype, city, country, people, person, state, street):
    """Create a new address in this addressbook, a new address key will be created."""
    api_obj = ctx_obj["api_obj"]
    params = {
        "addrtype": addrtype,
        "city": city,
        "country": country,
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
@click.option(
    "--addrtype",
    help="The address type, e.g. work or home",
    type=click.Choice(["work", "home"]),
    required=False,
)
@click.option("--city", help="The city of this address", type=str, required=False)
@click.option("--country", help="The country of this address", type=str, required=False)
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
    ctx_obj, address_key, addrtype, city, country, people, person, state, street
):
    """Update an existing address in this addressbook, with the given address key."""
    api_obj = ctx_obj["api_obj"]
    params = {
        "addrtype": addrtype,
        "city": city,
        "country": country,
        "people": people,
        "person": person,
        "state": state,
        "street": street,
    }

    req_body = update_addressbook_model.UpdateAddressbook(**params)
    resp = await api_obj.addressbook_address_key_put(address_key, req_body)
    _LOGGER.debug(f"resp: {resp}")

    if isinstance(resp, list):
        print(json.dumps([obj.to_dict() for obj in resp]))
        return

    print(json.dumps(resp.to_dict()) if resp else "None")


@main.group()
@click.pass_obj
def persons(ctx_obj):
    """High level command for an persons."""
    _LOGGER.debug(f"ctx_obj: {ctx_obj}")
    ctx_obj["api_obj"] = persons_api.PersonsApi(api_client=ctx_obj["api_client"])


# pylint: disable=redefined-builtin
@persons.command("create")
@click.option("--age", help="The person's age", type=int, required=False)
@click.option("--first-name", help="The person's first name", type=str, required=False)
@click.option("--hobbies", help="The person's hobbies", type=cli.StrList, required=False)
@click.option("--last-name", help="The person's last name", type=str, required=False)
@click.pass_obj
@firestone_utils.click_coro
@api_exc
async def persons_post(ctx_obj, age, first_name, hobbies, last_name):
    """Create a new person in this collection, a new UUID key will be created"""
    api_obj = ctx_obj["api_obj"]
    params = {
        "age": age,
        "first_name": first_name,
        "hobbies": hobbies,
        "last_name": last_name,
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
@click.option("--last-name", help="Filter by last name", type=str, required=False)
@click.option("--limit", help="Limit the number of responses back", type=int, required=False)
@click.option("--offset", help="The offset to start returning resources", type=int, required=False)
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
@click.pass_obj
@firestone_utils.click_coro
@api_exc
async def persons_uuid_put(ctx_obj, age, first_name, hobbies, last_name, uuid):
    """Put a new person in this collection, with the given UUId key"""
    api_obj = ctx_obj["api_obj"]
    params = {
        "age": age,
        "first_name": first_name,
        "hobbies": hobbies,
        "last_name": last_name,
    }

    req_body = update_person_model.UpdatePerson(**params)
    resp = await api_obj.persons_uuid_put(uuid, req_body)
    _LOGGER.debug(f"resp: {resp}")

    if isinstance(resp, list):
        print(json.dumps([obj.to_dict() for obj in resp]))
        return

    print(json.dumps(resp.to_dict()) if resp else "None")


@main.group()
@click.pass_obj
def postal_codes(ctx_obj):
    """High level command for an postal_codes."""
    _LOGGER.debug(f"ctx_obj: {ctx_obj}")
    ctx_obj["api_obj"] = postal_codes_api.PostalCodesApi(api_client=ctx_obj["api_client"])


# pylint: disable=redefined-builtin
@postal_codes.command("create")
@click.option("--name", help="The postal code's name/id", type=str, required=False)
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
@click.option("--limit", help="Limit the number of responses back", type=int, required=False)
@click.option("--name", help="Filter by name", type=str, required=False)
@click.option("--offset", help="The offset to start returning resources", type=int, required=False)
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


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    main()
