"""
Generate a rust, axum based server for the given resources.

Firestone already knows every path, method, model and security requirement in a
resource file, which is everything an HTTP server needs to exist.  This turns that
into a crate that compiles and runs: the router, the models, the middleware and
the RFC 9457 error handling, plus a ``Backend`` trait holding the one thing
firestone cannot know, which is where the data actually lives.

The rules declared by the resources are wired in too, so a generated handler
enforces them before it calls the backend.
"""

import logging

from firestone.spec import _base as spec_base
from firestone.spec import cli_rust
from firestone.spec import validations as spec_validations

_LOGGER = logging.getLogger(__name__)

#: JSON Schema types mapped to the rust types the generated models use.
TYPE_TO_RUST = {
    "string": "String",
    "integer": "i64",
    "number": "f64",
    "boolean": "bool",
}

#: Methods the generated router exposes on the collection.
RESOURCE_METHODS = ["get", "post"]

#: Methods the generated router exposes on a single resource.
INSTANCE_METHODS = ["get", "put", "patch", "delete"]

#: Methods the generated router exposes on one attribute of a resource.
#: HEAD is not listed because axum answers it wherever GET is routed.
ATTR_METHODS = ["get", "put", "delete"]

#: The crate firestone always writes, whether or not the resources declare rules.
TEMPLATES = [
    "Cargo.toml",
    "src/main.rs",
    "src/lib.rs",
    "src/error.rs",
    "src/models.rs",
    "src/backend.rs",
    "src/middleware.rs",
    "src/routes.rs",
    "src/handlers.rs",
    "tests/routes.rs",
]


def _rust_type(prop: dict) -> str:
    """Get the rust type for a single property of a resource.

    Anything firestone cannot name exactly, an embedded resource or a free form
    object, is carried as ``serde_json::Value`` rather than guessed at.
    """
    if "schema" in prop:
        nested = prop["schema"]
        # A property can carry its type under 'schema', or a whole embedded resource.
        if isinstance(nested, dict) and "items" not in nested and "type" in nested:
            return TYPE_TO_RUST.get(nested["type"], "serde_json::Value")

        return "serde_json::Value"

    prop_type = prop.get("type", "string")
    if prop_type == "array":
        items = prop.get("items", {})
        return f"Vec<{TYPE_TO_RUST.get(items.get('type', 'string'), 'serde_json::Value')}>"
    if prop_type == "object":
        return "serde_json::Value"

    return TYPE_TO_RUST.get(prop_type, "String")


def _properties(schema: dict) -> list:
    """Get the properties of a resource, in the shape the model template wants."""
    items = schema.get("items", {})
    required = items.get("required", [])
    properties = []

    for name in items.get("properties", {}):
        prop = items["properties"][name]
        if not isinstance(prop, dict):
            continue

        properties.append(
            {
                "name": name,
                "field": cli_rust._to_snake_case(name),  # pylint: disable=protected-access
                "type": _rust_type(prop),
                "required": name in required,
                "description": prop.get("description", ""),
            }
        )

    return properties


def _attrs(schema: dict) -> list:
    """Get the attributes that have their own endpoints.

    A property the schema hides with ``expose: false`` has no path of its own, the
    same rule the OpenAPI document follows.
    """
    properties = schema.get("items", {}).get("properties", {})

    return [
        name
        for name in properties
        if isinstance(properties[name], dict) and properties[name].get("expose", True)
    ]


def _query_params(rsrc: dict) -> list:
    """Get the query parameters the collection endpoint accepts."""
    params = []
    seen = set()

    for param in list(rsrc.get("default_query_params", [])) + list(
        rsrc.get("schema", {}).get("query_params", [])
    ):
        name = param["name"]
        if name in seen:
            continue
        seen.add(name)

        schema = param.get("schema", {"type": "string"})
        params.append(
            {
                "name": name,
                "field": cli_rust._to_snake_case(name),  # pylint: disable=protected-access
                "type": TYPE_TO_RUST.get(schema.get("type", "string"), "String"),
                "description": param.get("description", ""),
            }
        )

    return params


def _secured(security: dict, level: str) -> list:
    """Get the methods at this level that the schema says need authentication."""
    if not security or "scheme" not in security:
        return []

    return [method for method in security.get(level, []) if method]


def crate_version(version: str) -> str:
    """Get a semver crate version from the API version.

    An API version is often something like ``1.0``, which cargo will not take, so
    it is padded out rather than rejected.
    """
    parts = [part for part in str(version).split(".") if part.isdigit()]
    if not parts:
        return "0.1.0"

    return ".".join((parts + ["0", "0"])[:3])


def resources(rsrc_data: list, ruleset: dict = None) -> list:
    """Describe every resource in the shape the templates want.

    :param list rsrc_data: the resource data, as loaded from the resource files
    :param dict ruleset: the validation rules, so handlers know what to enforce
    :return: one entry per resource
    :rtype: list
    """
    ruleset = ruleset or {}
    described = []

    for rsrc in rsrc_data:
        kind = rsrc["kind"]
        schema = rsrc["schema"]
        singular = rsrc.get("singular") or spec_base.to_singular(kind)
        methods = rsrc.get("methods", {})
        security = rsrc.get("security", {})
        # pylint: disable=protected-access
        module = cli_rust._to_snake_case(kind)
        model = cli_rust._to_pascal_case(singular)

        key = schema.get("key", {})
        path = rsrc.get("plural") or kind
        if rsrc.get("versionInPath", False):
            path = f"v{rsrc['apiVersion']}/{path}"

        described.append(
            {
                "kind": kind,
                "module": module,
                "model": model,
                "path": path,
                "key": cli_rust._to_snake_case(key.get("name", "key")),
                "key_name": key.get("name", "key"),
                "description": rsrc.get("metadata", {}).get("description", kind),
                "properties": _properties(schema),
                "query_params": _query_params(rsrc),
                "resource_methods": [
                    method for method in RESOURCE_METHODS if method in methods.get("resource", [])
                ],
                "instance_methods": [
                    method for method in INSTANCE_METHODS if method in methods.get("instance", [])
                ],
                "attrs": _attrs(schema),
                "attr_methods": [
                    method for method in ATTR_METHODS if method in methods.get("instance_attrs", [])
                ],
                "secured_resource": _secured(security, "resource"),
                "secured_instance": _secured(security, "instance"),
                "secured_attrs": _secured(security, "instance_attrs"),
                "rules": kind in ruleset,
            }
        )

    return described


def generate(
    rsrc_data: list,
    title: str,
    desc: str,
    version: str,
    pkg: str = "api_server",
    ruleset: dict = None,
    with_validations: bool = True,
) -> dict:
    """Generate an axum server crate for the given resource data.

    :param list rsrc_data: the resource data, as loaded from the resource files
    :param str title: the title of the API
    :param str desc: the description of the API
    :param str version: the version of the API
    :param str pkg: the name of the generated crate
    :param dict ruleset: the validation rules, as returned by
        :func:`firestone.spec.validations.extract`
    :param bool with_validations: wire the validation package into the handlers
    :return: a mapping of file name to file contents
    :rtype: dict
    """
    described = resources(rsrc_data, ruleset if with_validations and ruleset else {})
    context = {
        "title": title,
        "description": desc,
        "version": version,
        "crate_version": crate_version(version),
        "pkg": pkg,
        "resources": described,
        "secured": any(
            rsrc["secured_resource"] or rsrc["secured_instance"] or rsrc["secured_attrs"]
            for rsrc in described
        ),
        "verbs": sorted(
            {method for rsrc in described for method in rsrc["resource_methods"]}
            | {method for rsrc in described for method in rsrc["instance_methods"]}
            | {method for rsrc in described for method in rsrc["attr_methods"]}
        ),
        "validations": bool(with_validations and ruleset),
    }
    _LOGGER.info(f"Generating an axum server for {len(described)} resource(s)")

    files = {
        name: spec_base.JINJA_ENV.get_template(f"server/rust/{name}.jinja2").render(**context)
        for name in TEMPLATES
    }

    if context["validations"]:
        tmpl = spec_base.JINJA_ENV.get_template("server/rust/src/resolver.rs.jinja2")
        files["src/resolver.rs"] = tmpl.render(**context)

        for name, content in spec_validations.generate(
            ruleset, language=spec_validations.LANG_RUST
        ).items():
            files[f"src/validation/{name}"] = content

    return {name: content.rstrip("\n") + "\n" for name, content in files.items()}
