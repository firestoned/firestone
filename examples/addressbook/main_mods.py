#!/usr/bin/env python
"""
Main entry point for a click based CLI.
"""

import importlib
import logging
import os
import pkgutil
import sys

import click

from addressbook.client import configuration


def make_commands(pkg, **click_args):
    """Make a Click multicommand from all submodules of the module."""

    class MCommand(click.MultiCommand):
        """Treadmill CLI driver."""

        def __init__(self, *args, **kwargs):
            if kwargs and click_args:
                kwargs.update(click_args)

            click.MultiCommand.__init__(self, *args, **kwargs)

        def list_commands(self, ctx):
            """Return list of commands in pkg."""
            path = pkg.replace(".", os.sep)
            modules = [name for _, name, _ in pkgutil.iter_modules([path])]
            return sorted(modules)

        def get_command(self, ctx, cmd_name):
            """Return dymanically constructed command."""
            try:
                return importlib.import_module(f"{pkg}.{cmd_name}").init()
            except ImportError as import_err:
                print("dependency error: {pkg}.{cmd_name}: {import_err}", file=sys.stderr)
            except KeyError:
                raise click.UsageError(f"Invalid command: {cmd_name}")

    return MCommand


@click.group(cls=make_commands("addressbook.cli"))
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

    ctx.obj = {
        "api_client_config": config,
    }


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    main()
