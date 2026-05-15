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


def to_singular(name: str) -> str:
    """Convert a plural resource name to its singular form.

    Handles common English pluralization patterns. For irregular cases,
    callers should prefer an explicit ``singular`` key in the resource schema.
    """
    if name.endswith(("ses", "xes", "ches", "shes", "zes")):
        return name[:-2]  # addresses -> address, boxes -> box
    if name.endswith("ies") and len(name) > 3:
        return name[:-3] + "y"  # categories -> category
    if name.endswith("s") and not name.endswith("ss"):
        return name[:-1]  # books -> book  (but "class" stays "class")
    return name


def get_opid(path: str, method: str):
    """Get a unique operationId given the path and method."""
    opid = path[1:].replace("/", "_")
    opid = opid.replace("{", "")
    opid = opid.replace("}", "")
    return f"{opid}_{method}"
