"""
The main entry point for firestone.
"""

import io
import logging
import os

import click

from firestone_lib import cli as firestone_cli
from firestone_lib import resource as firestone_rsrc

from firestone import spec as firestone_spec

_LOGGER = logging.getLogger(__name__)


@click.group()
@click.option("--debug", help="Turn on debugging", is_flag=True)
def main(debug):
    """Main entry point"""
    firestone_cli.init_logging("firestone_lib.resources.logging", "cli.conf")

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
    type=firestone_cli.PathList,
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
@click.option(
    "--version",
    "-v",
    help="The overall version of this spec",
    required=True,
)
@click.pass_context
def generate(ctx, description, resources, summary, title, version):
    """Upper command for gathering common resource information for the generators."""
    ctx.obj = {
        "data": [],
        "desc": description,
        "summary": summary,
        "title": title,
        "version": version,
    }
    for rsrc in resources:
        _LOGGER.debug(f"rsrc: {rsrc}")
        rsrc_data = firestone_rsrc.get_resource_schema(rsrc)
        _LOGGER.debug(f"rsrc_data: {rsrc_data}")
        _LOGGER.info(f"Validating resource {rsrc_data['kind']} against firestone JSON schema.")
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
@click.option(
    "--version",
    help="Set the OpenAPI spec version",
    show_default=True,
    default=firestone_spec.openapi.DEFAULT_VERSION,
)
@click.pass_obj
def openapi(rsrc_data, output, ui_server, prefix, version):
    """Generate an OpenAPI specification for the given resource data."""

    openapi_spec = firestone_spec.openapi.generate(
        rsrc_data["data"],
        rsrc_data["title"],
        rsrc_data["desc"],
        rsrc_data["summary"],
        rsrc_data["version"],
        prefix=prefix,
        openapi_version=version,
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

    asyncapi_spec = firestone_spec.asyncapi.generate(
        rsrc_data["data"],
        rsrc_data["title"],
        rsrc_data["desc"],
        rsrc_data["summary"],
        rsrc_data["version"],
    )
    print(asyncapi_spec, file=output)


@generate.command()
@click.option(
    "--output",
    "-O",
    help="Location of the main CLI generated file name, or `-` for stdout",
    type=click.File("w"),
    default="-",
    show_default=True,
)
@click.option(
    "--output-dir",
    "-o",
    help="Location of the directory to output the CLI generated module files",
    type=click.Path(file_okay=False, dir_okay=True, writable=True),
)
@click.option(
    "--as-modules",
    help="Output each resource as a module",
    is_flag=True,
)
@click.option(
    "--pkg",
    help="The package where the OpenAPI client code is.",
    required=True,
)
@click.option(
    "--client-pkg",
    help="The package where the OpenAPI client code is.",
    required=True,
)
@click.option(
    "--template",
    "-T",
    help="The location of a custom template to render the resources for CLI",
    type=str,
)
@click.pass_obj
def cli(rsrc_data, pkg, client_pkg, output, output_dir, as_modules, template):
    """Generate python, Click-based CLI script.

    This generated script can be used as standalone or added to console scripts.
    """
    cli_spec = firestone_spec.cli.generate(
        pkg,
        client_pkg,
        rsrc_data["data"],
        rsrc_data["title"],
        rsrc_data["desc"],
        rsrc_data["summary"],
        rsrc_data["version"],
        as_modules,
        template=template,
    )
    if not as_modules:
        return print(cli_spec, file=output)

    if not output_dir:
        raise click.UsageError("You must supply an --output-dir when using --as-modules")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for rsrc in cli_spec:
        with io.open(os.path.join(output_dir, f"{rsrc}.py"), "w", encoding="utf-8") as fh:
            fh.write(cli_spec[rsrc])

    return None


@generate.command()
@click.option(
    "--as-modules",
    help="Output each resource as a module",
    is_flag=True,
)
@click.option(
    "--backend-url",
    help="The default backend base URL for API",
    default="https://localhost",
)
@click.option(
    "--col-mappings",
    "-C",
    help="Custom column mapping orders, e.g. {'addressbook': ['postal_code', '']",
    type=firestone_cli.AnyDict,
)
@click.option(
    "--output",
    "-O",
    help="Location of the main CLI generated file name, or `-` for stdout",
    type=click.File("w"),
    default="-",
    show_default=True,
)
@click.option(
    "--output-dir",
    "-o",
    help="Location of the directory to output the CLI generated module files",
    type=click.Path(file_okay=False, dir_okay=True, writable=True),
)
@click.option(
    "--template",
    "-T",
    help="The location of a custom template to render the resources for CLI",
    type=str,
)
@click.pass_obj
def streamlit(rsrc_data, backend_url, col_mappings, output, output_dir, as_modules, template):
    """Generate python, Click-based CLI script.

    This generated script can be used as standalone or added to console scripts.
    """
    _LOGGER.debug(f"col_mappings: {col_mappings}")
    st_spec = firestone_spec.streamlit.generate(
        rsrc_data["data"],
        rsrc_data["title"],
        rsrc_data["desc"],
        rsrc_data["summary"],
        rsrc_data["version"],
        backend_url=backend_url,
        as_modules=as_modules,
        template=template,
        col_mappings=col_mappings,
    )

    if not as_modules:
        return print(st_spec, file=output)

    if not output_dir:
        raise click.UsageError("You must supply an --output-dir when using --as-modules")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for rsrc in st_spec:
        with io.open(os.path.join(output_dir, f"{rsrc}.py"), "w", encoding="utf-8") as fh:
            fh.write(st_spec[rsrc])

    return None


if __name__ == "main":
    # pylint: disable=no-value-for-parameter
    main()
