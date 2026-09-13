"""
Generate the glue between a rust-axum server and your storage.

The server itself is not firestone's to write: ``openapi-generator -g rust-axum``
already turns the OpenAPI document firestone produces into a router, typed models,
per-operation authentication and request validation.  What it leaves behind is a
set of traits with one required method per operation, and for a real API that is
dozens of methods that have to exist before anything compiles.

This generates those: every trait method, wired to a ``Backend`` trait that is the
one thing firestone cannot know, plus the adapter that lets the validation rules
reach the same backend.  Everything here is derived from the same OpenAPI document
the server was generated from, so the two cannot disagree about a name.
"""

import json
import logging
import re

import yaml

from firestone.spec import _base as spec_base
from firestone.spec import openapi as spec_openapi
from firestone.spec import validations as spec_validations

_LOGGER = logging.getLogger(__name__)

#: JSON Schema types mapped the way openapi-generator's rust-axum maps them.
TYPE_TO_RUST = {
    "string": "String",
    "integer": "i32",
    "number": "f64",
    "boolean": "bool",
}

#: Formats that change the rust type. An int64 that came through as i32 would not
#: satisfy the trait the generated server declares.
FORMAT_TO_RUST = {
    ("integer", "int32"): "i32",
    ("integer", "int64"): "i64",
    ("number", "float"): "f32",
    ("number", "double"): "f64",
}


def rust_type(schema: dict) -> str:
    """Get the rust type openapi-generator would choose for a scalar schema."""
    kind = schema.get("type")
    fmt = schema.get("format")

    return FORMAT_TO_RUST.get((kind, fmt)) or TYPE_TO_RUST.get(kind)


#: The methods that carry a body, and so can be validated.
MUTATING = ["post", "put", "patch", "delete"]


#: Convert a name the way openapi-generator does, keeping inner capitals, so
#: ``create_postal_code`` becomes ``CreatePostalCode`` and ``OK`` stays ``OK``.
pascal = spec_base.pascal


def variant(code, description: str) -> str:
    """Get the response enum variant openapi-generator generates for a response."""
    status = 0 if code == "default" else code
    words = "".join(word[0].upper() + word[1:] for word in str(description).split() if word)

    return f"Status{status}_{words}"


def _body_type(operation: dict) -> str:
    """Get the rust type of an operation's request body, if it has one."""
    body = operation.get("requestBody")
    if not body:
        return None

    schema = body.get("content", {}).get(spec_base.DEFAULT_CONTENT_TYPE, {}).get("schema", {})
    if "$ref" in schema:
        return f"models::{pascal(schema['$ref'].rsplit('/', 1)[-1])}"

    if schema.get("type") == "array":
        items = schema.get("items", {})
        if "$ref" in items:
            return f"Vec<models::{pascal(items['$ref'].rsplit('/', 1)[-1])}>"

        return f"Vec<{rust_type(items) or 'serde_json::Value'}>"

    # A type firestone does not map falls back to Value, which will not match what
    # openapi-generator chose and so fails to compile rather than misbehaving. That
    # is the right way round: firestone controls the schema this was built from.
    return rust_type(schema) or "serde_json::Value"


def _success(operation: dict) -> dict:
    """Get the response a handler returns when nothing went wrong."""
    for code in sorted(operation.get("responses", {}), key=str):
        if str(code) in ("200", "201") or code == "default":
            response = operation["responses"][code]

            return {
                "variant": variant(code, response.get("description", "")),
                "payload": bool(response.get("content")),
            }

    return None


#: What a handler does, by path shape and method. An action absent from this table
#: is one firestone will not guess at: a POST to an embedded collection appends and
#: a PATCH merges, and neither is a replace.
_ACTIONS = {
    ("collection", "get"): "list",
    ("collection", "post"): "create",
    ("instance", "get"): "fetch",
    ("instance", "put"): "update",
    ("instance", "patch"): "update",
    ("instance", "delete"): "remove",
    ("attribute", "get"): "attr_get",
    ("attribute", "put"): "attr_set",
    ("attribute", "delete"): "attr_remove",
}

#: The actions that cannot run without a request body to apply.
_NEEDS_BODY = ["create", "update", "attr_set"]


def _action(shape: str, method: str, body: str, success: dict) -> str:
    """Get what a handler for this operation should do, or None if firestone cannot say.

    The template dispatches on this rather than re-deriving it, so the set of
    operations firestone claims to implement cannot drift from the set it actually
    writes a body for.
    """
    if not success:
        return None
    if method == "head":
        return "head"

    action = _ACTIONS.get((shape, method))
    if action in _NEEDS_BODY and not body:
        return None

    return action


#: The actions whose handler deserializes what the backend returned.
_READS = ["list", "create", "fetch", "update", "attr_get"]

#: The actions whose handler serializes the request body.
_WRITES = _NEEDS_BODY


#: A value of each JSON Schema type, for the body the generated tests post.
_SAMPLES = {"string": "x", "integer": 1, "number": 1.5, "boolean": True, "array": []}


def _model(spec: dict, body_type: str) -> tuple:
    """Resolve a request model to its properties and its required fields.

    Create models are ``allOf[base, {required: [...]}]``, so both halves matter.
    """
    if not body_type or not body_type.startswith("models::"):
        return {}, []

    schemas = spec.get("components", {}).get("schemas", {})
    wanted = body_type.split("::", 1)[1]
    model = next((schemas[name] for name in schemas if pascal(name) == wanted), None)
    if not model:
        return {}, []

    required = []
    base = {}
    for part in model.get("allOf", [model]):
        required.extend(part.get("required", []))
        if "$ref" in part:
            ref = part["$ref"].rsplit("/", 1)[-1]
            base = schemas.get(ref, {}).get("properties", {})
        else:
            base.update(part.get("properties", {}))

    return base, required


def _sample_body(spec: dict, body_type: str) -> dict:
    """Build a body satisfying the required fields of a create's request model.

    The generated tests have to post something the request validation accepts, and
    what that is comes from the document rather than from guesswork.
    """
    base, required = _model(spec, body_type)

    body = {}
    for name in required:
        prop = base.get(name, {})
        if prop.get("enum"):
            body[name] = prop["enum"][0]
        else:
            body[name] = _SAMPLES.get(prop.get("type", "string"), "x")

    return body


def _shape(path: str) -> dict:
    """Work out what a path is, so a handler knows which backend call it maps to."""
    parts = [part for part in path.strip("/").split("/") if part]
    keys = [part for part in parts if part.startswith("{")]
    trailing = parts[-1]

    if not keys:
        return {"kind": "collection", "attr": None}
    if trailing.startswith("{"):
        return {"kind": "instance", "attr": None}

    # A path segment after the key is an attribute of the resource, which the
    # OpenAPI document exposes in its own right.
    return {"kind": "attribute", "attr": trailing}


def _returnable_key(spec: dict, ops: list) -> str:
    """Get the key attribute a create can hand back, if the model declares one.

    The response goes through the typed model, and serde drops a field the struct
    does not have, so a key the item schema never declared cannot come back. A
    resource that wants its key in responses declares it as a property, as the
    addressbook example does.
    """
    key = next((op["key"] for op in sorted(ops, key=lambda o: o["name"]) if op["key"]), None)
    if not key:
        return None

    create = next((op for op in ops if op["action"] == "create"), None)
    properties, _ = _model(spec, create["body"] if create else None)

    return key if key in properties else None


def operations(spec: dict, ruleset: dict) -> dict:
    """Describe every operation the generated server expects an implementation of.

    :param dict spec: the OpenAPI document, as generated by firestone
    :param dict ruleset: the validation rules, so a handler knows what to enforce
    :return: the operations, grouped by the trait that declares them
    :rtype: dict
    """
    traits = {}

    for path in spec.get("paths", {}):
        for method in spec["paths"][path]:
            operation = spec["paths"][path][method]
            if not isinstance(operation, dict) or "operationId" not in operation:
                continue

            tag = (operation.get("tags") or ["default"])[0]
            params = operation.get("parameters") or []
            shape = _shape(path)
            path_params = [param for param in params if param.get("in") == "path"]

            success = _success(operation)
            body = _body_type(operation)
            action = _action(shape["kind"], method, body, success)
            traits.setdefault(tag, []).append(
                {
                    "name": operation["operationId"],
                    "response": f"{pascal(operation['operationId'])}Response",
                    "method": method,
                    "path": path,
                    # The same path with its parameters filled in, so a generated
                    # test can ask for it without any string surgery of its own.
                    "test_path": re.sub(r"\{[^}]+\}", "test-key", path),
                    "resource": tag,
                    "shape": shape["kind"],
                    "attr": shape["attr"],
                    "key": path_params[-1]["name"] if path_params else None,
                    "claims": bool(operation.get("security")),
                    "path_params": bool(path_params),
                    "query_params": any(param.get("in") == "query" for param in params),
                    "body": body,
                    "success": success,
                    "rules": tag in ruleset and method in MUTATING,
                    # Whether firestone knows how to answer this operation. One it
                    # does not, such as a mutating operation the document declares
                    # no body for, is left explicit rather than guessed at.
                    "action": action,
                    "implemented": bool(action),
                    # Whether the generated body actually reads the key, so the
                    # argument is not bound to a name nothing uses.
                    "uses_key": bool(path_params)
                    and action not in (None, "head", "list", "create"),
                    # Whether the generated body reads the request body, so the
                    # argument is not bound to a name nothing uses.
                    "uses_body": bool(body) and action in _WRITES,
                }
            )

    return {
        tag: {
            "module": tag,
            "trait": pascal(tag),
            # The attribute the resource is keyed by, taken from its instance path.
            # A create returns the body it was given, so the key the backend minted
            # has to be put into it before it goes back.
            # A body the request validation will accept, for the generated tests.
            "sample_body": json.dumps(
                _sample_body(
                    spec,
                    next(
                        (
                            op["body"]
                            for op in sorted(traits[tag], key=lambda o: o["name"])
                            if op["action"] == "create"
                        ),
                        None,
                    ),
                )
            ),
            "key_field": _returnable_key(spec, traits[tag]),
            # Only a trait with a secured operation declares the associated Claims
            # type, so implementing it unconditionally does not compile.
            "claims": any(op["claims"] for op in traits[tag]),
            "operations": sorted(traits[tag], key=lambda op: op["name"]),
        }
        for tag in sorted(traits)
    }


def _doc(text: str) -> str:
    """Flatten text for a doc comment, where a newline would end the comment."""
    return " ".join(str(text).split())


def _rust_format(text: str) -> str:
    """Escape text for the inside of a rust format string.

    Quotes and backslashes have to be escaped as in any rust literal, and braces
    doubled, or a title containing one is read as a format argument.
    """
    escaped = json.dumps(str(text))[1:-1]

    return escaped.replace("{", "{{").replace("}", "}}")


def _context(spec: dict, ruleset: dict, names: dict) -> dict:
    """Build what the templates are rendered with.

    :param dict spec: the OpenAPI document the server was generated from
    :param dict ruleset: the rules to enforce, empty when they are turned off
    :param dict names: the title, description, version and crate names
    """
    traits = operations(spec, ruleset)
    every = [op for trait in traits.values() for op in trait["operations"]]

    return {
        **names,
        "crate_version": crate_version(names["version"]),
        "traits": traits,
        "validations": bool(ruleset),
        # An operation is only secured if the schema said so, and the generated
        # server only declares ApiAuthBasic when something is, so generating an
        # implementation of it unconditionally does not compile.
        "secured": any(op["claims"] for op in every),
        # Imported only where the handlers reach for them: an unused import is a
        # warning, and the gate treats warnings as errors.
        "needs_value": any(op["action"] == "list" for op in every)
        or any(
            trait["key_field"] and op["action"] == "create"
            for trait in traits.values()
            for op in trait["operations"]
        ),
        # models is reached for by the path and query parameter types in the
        # signature as well as by a request body, so a schema with an instance path
        # and no body still needs it.
        "needs_models": any(op["body"] or op["path_params"] or op["query_params"] for op in every),
        "needs_to_json": any(op["action"] in _WRITES for op in every),
        # Whether there is anything to test. A resource with, say, only a create has
        # no round trip to check and no credentials to refuse, and a test file of
        # nothing but unused helpers does not compile.
        # json! is only used by the create round trip and the secured-operation
        # checks, so a file carrying neither must not import it.
        "needs_json": any(
            trait["key_field"]
            and any(op["action"] == "create" for op in trait["operations"])
            and any(op["action"] == "fetch" for op in trait["operations"])
            for trait in traits.values()
        )
        or any(op["claims"] and op["action"] for op in every),
        "has_tests": any(
            trait["key_field"]
            and any(op["action"] == "create" for op in trait["operations"])
            and any(op["action"] == "fetch" for op in trait["operations"])
            for trait in traits.values()
        )
        or any(op["claims"] and op["action"] for op in every)
        or any(op["action"] == "fetch" and not op["claims"] for op in every),
        "needs_from_json": any(
            op["action"] in _READS
            or (op["action"] in ("remove", "attr_set", "attr_remove") and op["success"]["payload"])
            for op in every
        ),
    }


def generate(
    rsrc_data: list,
    title: str,
    desc: str,
    version: str,
    pkg: str = "api_server",
    api_pkg: str = "openapi",
    ruleset: dict = None,
    with_validations: bool = True,
) -> dict:
    """Generate the implementation crate for a rust-axum server.

    :param list rsrc_data: the resource data, as loaded from the resource files
    :param str title: the title of the API
    :param str desc: the description of the API
    :param str version: the version of the API
    :param str pkg: the name of the generated crate
    :param str api_pkg: the crate name openapi-generator was given
    :param dict ruleset: the validation rules, as returned by
        :func:`firestone.spec.validations.extract`
    :param bool with_validations: enforce those rules in the generated handlers
    :return: a mapping of file name to file contents
    :rtype: dict
    """
    ruleset = (ruleset or {}) if with_validations else {}

    # Derived from the document the server was generated from, rather than from the
    # resources directly, so firestone and openapi-generator cannot disagree about
    # an operation id, a model name or a response variant.
    spec = yaml.safe_load(spec_openapi.generate(rsrc_data, title, desc, desc, version))
    context = _context(
        spec,
        ruleset,
        {
            # User text, landing in a TOML string, a rust format string and a doc
            # comment, so each gets a form that cannot break its surroundings.
            "title": _doc(title),
            "title_toml": json.dumps(title),
            "title_fmt": _rust_format(title),
            "description": _doc(desc),
            "description_toml": json.dumps(desc),
            "version": version,
            "pkg": pkg,
            "api_pkg": api_pkg,
        },
    )
    _LOGGER.info(
        f"Generating an implementation of {len(context['traits'])} trait(s) "
        f"for {context['pkg']}"
    )

    files = {
        name: spec_base.JINJA_ENV.get_template(f"server/rust/{name}.jinja2").render(**context)
        for name in TEMPLATES
        if (name != "src/auth.rs" or context["secured"])
        and (name != "tests/api.rs" or context["has_tests"])
    }

    if context["validations"]:
        tmpl = spec_base.JINJA_ENV.get_template("server/rust/src/resolver.rs.jinja2")
        files["src/resolver.rs"] = tmpl.render(**context)

        for name, content in spec_validations.generate(
            ruleset, language=spec_validations.LANG_RUST
        ).items():
            files[f"src/validation/{name}"] = content

    return {name: content.rstrip("\n") + "\n" for name, content in files.items()}


def crate_version(version: str) -> str:
    """Get a semver crate version from the API version.

    An API version is often something like ``1.0``, which cargo will not take, so
    it is padded out rather than rejected.
    """
    parts = [part.lstrip("vV") for part in str(version).split(".")]
    parts = [part for part in parts if part.isdigit()]
    if not parts:
        return "0.1.0"

    return ".".join((parts + ["0", "0"])[:3])


#: Regenerated every time, because they follow the OpenAPI document exactly.
#:
#: lib.rs is here because the modules it declares depend on the document: turning
#: on security or validations adds auth.rs and resolver.rs, and a kept lib.rs would
#: not declare them, leaving a crate that does not compile.
GENERATED = ["src/handlers.rs", "src/lib.rs", "tests/api.rs"]

#: Written once, then yours. Firestone will not overwrite these unless asked, so
#: the Backend you implement and the tokens you accept survive a regeneration.
SCAFFOLD = [
    "Cargo.toml",
    "src/main.rs",
    "src/error.rs",
    "src/backend.rs",
    "src/auth.rs",
]

#: Every template, in the order they are rendered.
TEMPLATES = GENERATED + SCAFFOLD
