"""
The main entry point for firestone.
"""
import logging

import click

from firestone_lib import cli

from firestone import resource as firestone_rsrc
from firestone import spec as firestone_spec

_LOGGER = logging.getLogger(__name__)


@click.group()
@click.option("--debug", help="Turn on debugging", is_flag=True)
def main(debug):
    """Main entry point"""
    cli.init_logging("firestone_lib.resources.logging", "cli.conf")

    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.getLogger("firestone").setLevel(logging.DEBUG)


@main.group()
@click.option(
    "--description",
    "-d",
    help="The description of this project",
    required=True,
)
@click.option(
    "--resources",
    "-r",
    help="One or more resource files in JSON Schema format, can be JSON or YAML",
    required=True,
    type=cli.PathList,
)
@click.option(
    "--summary",
    "-s",
    help="The summary of this project, defaults to description",
)
@click.option(
    "--title",
    "-t",
    help="The title of this project",
    required=True,
)
@click.pass_context
def generate(ctx, description, resources, summary, title):
    """Upper command for gathering common resource information for the generators."""
    ctx.obj = {
        "data": [],
        "desc": description,
        "summary": summary,
        "title": title,
    }
    for rsrc in resources:
        _LOGGER.debug(f"rsrc: {rsrc}")
        rsrc_data = firestone_rsrc.get_resource_schema(rsrc)
        _LOGGER.info(f"Validating resource {rsrc_data['name']} against firestone JSON schema.")
        firestone_rsrc.validate(rsrc_data)

        ctx.obj["data"].append(rsrc_data)


# TODO add support for providing an existing openapi spec file and merge data in
@generate.command()
@click.option(
    "--output",
    "-O",
    help="Output the specificaton to file name provided, or `-` for stdout",
    type=click.File("w"),
    default="-",
)
@click.option(
    "--ui-server",
    help="Launch web server to vierw Swagger UI",
    is_flag=True,
)
@click.option(
    "--prefix",
    help="A prefix to all URLs, this will add a 'servers' section to the openapi spec doc",
)
@click.pass_obj
def openapi(rsrc_data, output, ui_server, prefix):
    """Generate an OpenAPI specification for the given resource data."""

    openapi_spec = firestone_spec.openapi.generate(
        rsrc_data["data"], rsrc_data["title"], rsrc_data["desc"], rsrc_data["summary"], prefix=prefix,
    )
    print(openapi_spec, file=output)

    if ui_server:
        # pylint: disable=import-outside-toplevel,import-error,no-member
        import quart
        import swagger_ui

        app = quart.Quart(__name__)
        swagger_ui.quart_api_doc(
            app, config_spec=openapi_spec, url_prefix="/apidocs", title="OpenAPI doc"
        )

        app.run()


@generate.command()
@click.option(
    "--output",
    "-O",
    help="Output the specificaton to file name provided, or `-` for stdout",
    type=click.File("w"),
    default="-",
)
@click.pass_obj
def asyncapi(rsrc_data, output):
    """Generate an AsyncAPI specification for the given resource data."""

    openapi_spec = firestone_spec.asyncapi.generate(
        rsrc_data["data"], rsrc_data["title"], rsrc_data["desc"], rsrc_data["summary"]
    )
    print(openapi_spec, file=output)


if __name__ == "main":
    # pylint: disable=no-value-for-parameter
    main()
