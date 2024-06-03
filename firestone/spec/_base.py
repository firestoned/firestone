"""
Base functions for managing spec files
"""

import jinja2
import yaml

DEFAULT_CONTENT_TYPE = "application/json"

JINJA_ENV = jinja2.Environment(
    loader=jinja2.PackageLoader("firestone", package_path="schema"),
    autoescape=jinja2.select_autoescape(),
    extensions=["jinja2.ext.loopcontrols"],
)


class SchemaMissingAttribute(Exception):
    """Schema is missing an attribute."""


def yaml_pretty(data, indent=2):
    """A simple YAML pretty print for Jinja."""
    dump = yaml.dump(data, indent=2)
    res = ""
    for line in dump.split("\n"):
        res += " " * indent + line + "\n"
    return res.rstrip()


JINJA_ENV.filters["yaml_pretty"] = yaml_pretty


def get_opid(path: str, method: str):
    """Get a unique operationId given the path and method."""
    opid = path[1:].replace("/", "_")
    opid = opid.replace("{", "")
    opid = opid.replace("}", "")
    return f"{opid}_{method}"
