"""
Extract and generate optional, declarative validations for resources.

Firestone resources can declare two kinds of validation, both entirely optional:

1. ``references`` on a property, which declares a relationship to another
   resource.  This desugars into ``exists`` and ``immutable`` rules.
2. A top level ``validations.rules`` list, where each rule declares the lookups
   it needs and a `CEL <https://github.com/google/cel-spec>`_ expression over
   ``self``, ``old``, ``refs`` and ``ctx``.

Both lower into the same normalised rule structure, which is what gets emitted
into the OpenAPI document as ``x-firestone-validations`` and rendered into the
generated validation package.

Firestone never performs the lookups itself: it only knows *what* each rule
needs.  The generated package exposes a ``Resolver`` interface for the consumer
to implement against their own database or cache.
"""

import copy
import json
import logging
import re

from firestone.spec import _base as spec_base

_LOGGER = logging.getLogger(__name__)

#: The HTTP methods a rule may be attached to.
RULE_METHODS = ["post", "put", "patch", "delete"]

#: Methods a rule runs on when it does not say otherwise.
DEFAULT_METHODS = {
    "exists": ["post", "put", "patch"],
    "immutable": ["put", "patch"],
    "expr": ["post", "put", "patch"],
}

#: The vendor extension the rules are emitted under in the OpenAPI document.
OPENAPI_EXTENSION = "x-firestone-validations"

#: The component name of the RFC 9457 problem document returned on failure.
PROBLEM_COMPONENT = "ValidationProblem"

#: The languages a validation package can be generated for.
LANG_PYTHON = "python"
LANG_RUST = "rust"
LANGUAGES = [LANG_PYTHON, LANG_RUST]

_RULE_KINDS = ["exists", "immutable", "expr"]
_REFERENCE_KEYS = {"kind", "key", "value", "on_missing", "immutable", "description"}
_RULE_KEYS = {"name", "description", "methods", "refs", "expr", "error", "examples"}
_REF_KEYS = {"kind", "key", "value", "optional"}
_ERROR_KEYS = {"status", "message"}
_NAME_RE = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")


class InvalidValidation(Exception):
    """A resource declares a validation that firestone cannot make sense of."""


def _check_keys(where: str, data: dict, allowed: set):
    """Raise if ``data`` carries a key firestone does not understand."""
    unknown = sorted(set(data) - allowed)
    if unknown:
        raise InvalidValidation(
            f"{where}: unknown key(s) {', '.join(unknown)}; expected one of "
            f"{', '.join(sorted(allowed))}"
        )


def _check_methods(where: str, methods: list):
    """Raise if ``methods`` names an HTTP method a rule cannot attach to."""
    if not isinstance(methods, list) or not methods:
        raise InvalidValidation(f"{where}: 'methods' must be a non-empty list of HTTP methods")

    bad = sorted({method for method in methods if method not in RULE_METHODS})
    if bad:
        raise InvalidValidation(
            f"{where}: cannot validate on {', '.join(bad)}; "
            f"rules only run on {', '.join(RULE_METHODS)}"
        )


def _default_key(kinds: dict, kind: str, where: str) -> str:
    """Get the key attribute of the referenced resource, its schema key by default.

    Firestone can only work this out for a resource it was given.  Rather than hand
    the resolver a lookup with no key and let it fail at request time, a reference
    to a resource generated elsewhere has to say which key to match on.
    """
    target = kinds.get(kind)
    if target is None:
        raise InvalidValidation(
            f"{where}: references '{kind}', which is not one of the resources given to "
            "firestone, so its key cannot be worked out. Pass that resource file too, or "
            "give this reference an explicit 'key'."
        )

    key = target.get("schema", {}).get("key", {}).get("name")
    if not key:
        raise InvalidValidation(
            f"{where}: references '{kind}', which has no schema key, so give this "
            "reference an explicit 'key'."
        )

    return key


def _normalise_ref(where: str, name: str, ref: dict, kinds: dict) -> dict:
    """Normalise a single ``refs`` entry into its generated form."""
    if not isinstance(ref, dict):
        raise InvalidValidation(f"{where}: ref '{name}' must be a mapping")
    _check_keys(f"{where}, ref '{name}'", ref, _REF_KEYS)

    if not _NAME_RE.match(name):
        raise InvalidValidation(
            f"{where}: ref name '{name}' must be a valid identifier, so that it can be "
            "referred to as refs.{name} in an expression"
        )
    if "kind" not in ref:
        raise InvalidValidation(f"{where}, ref '{name}': a 'kind' is required")
    if "value" not in ref:
        raise InvalidValidation(
            f"{where}, ref '{name}': a 'value' is required, the dotted path in the request "
            "body holding the value to look up, e.g. person.first_name"
        )

    kind = ref["kind"]
    optional = ref.get("optional", False)
    if not isinstance(optional, bool):
        raise InvalidValidation(f"{where}, ref '{name}': 'optional' must be true or false")

    return {
        "name": name,
        "kind": kind,
        "key": ref.get("key") or _default_key(kinds, kind, f"{where}, ref '{name}'"),
        "value": ref["value"],
        "optional": optional,
    }


def _normalise_error(where: str, error: dict, default_status: int, default_message: str) -> dict:
    """Normalise a rule's ``error`` block, filling in the defaults."""
    if error is None:
        error = {}
    if not isinstance(error, dict):
        raise InvalidValidation(f"{where}: 'error' must be a mapping")
    _check_keys(f"{where}, error", error, _ERROR_KEYS)

    status = error.get("status", default_status)
    if not isinstance(status, int) or not 400 <= status <= 599:
        raise InvalidValidation(f"{where}: error status {status} is not a 4xx or 5xx status code")

    return {"status": status, "message": error.get("message", default_message)}


def _reference_rules(rsrc_kind: str, prop: str, ref: dict, kinds: dict) -> list:
    """Desugar a property level ``references`` block into rules."""
    where = f"{rsrc_kind}.{prop}.references"
    if not isinstance(ref, dict):
        raise InvalidValidation(f"{where}: must be a mapping")
    _check_keys(where, ref, _REFERENCE_KEYS)

    if "kind" not in ref:
        raise InvalidValidation(f"{where}: a 'kind' is required, the resource being referenced")

    on_missing = ref.get("on_missing", "reject")
    if on_missing not in ("reject", "ignore"):
        raise InvalidValidation(
            f"{where}: on_missing must be 'reject' or 'ignore', not '{on_missing}'"
        )

    kind = ref["kind"]
    value = ref.get("value", prop)
    key = ref.get("key") or _default_key(kinds, kind, where)
    rules = []

    if on_missing == "reject":
        rules.append(
            {
                "name": f"{prop}_must_exist",
                "description": ref.get("description", f"The referenced {kind} must already exist."),
                "resource": rsrc_kind,
                "kind": "exists",
                "field": value,
                "methods": list(DEFAULT_METHODS["exists"]),
                "refs": [
                    {
                        "name": prop,
                        "kind": kind,
                        "key": key,
                        "value": value,
                        "optional": False,
                    }
                ],
                "expr": None,
                "error": {
                    "status": 422,
                    "message": f"No {kind} found with {key} '{{self.{value}}}'.",
                },
                "examples": [],
            }
        )

    if ref.get("immutable", False):
        rules.append(
            {
                "name": f"{prop}_is_immutable",
                "description": f"The reference to {kind} cannot be changed after creation.",
                "resource": rsrc_kind,
                "kind": "immutable",
                "field": value,
                "methods": list(DEFAULT_METHODS["immutable"]),
                "refs": [],
                "expr": None,
                "error": {
                    "status": 409,
                    "message": f"{value} is immutable and cannot be changed.",
                },
                "examples": [],
            }
        )

    return rules


def _normalise_examples(where: str, examples: list) -> list:
    """Normalise a rule's ``examples``, used to generate a test suite."""
    if not examples:
        return []
    if not isinstance(examples, list):
        raise InvalidValidation(f"{where}: 'examples' must be a list")

    out = []
    for idx, example in enumerate(examples):
        if not isinstance(example, dict):
            raise InvalidValidation(f"{where}, example {idx}: must be a mapping")
        expect = example.get("expect")
        if expect not in ("pass", "fail"):
            raise InvalidValidation(
                f"{where}, example {idx}: 'expect' must be 'pass' or 'fail', not {expect!r}"
            )
        out.append(
            {
                "self": example.get("self", {}),
                "old": example.get("old"),
                "refs": example.get("refs", {}),
                "ctx": example.get("ctx", {}),
                "expect": expect,
            }
        )

    return out


def _expr_rule(rsrc_kind: str, rule: dict, kinds: dict) -> dict:
    """Normalise a single entry of the top level ``validations.rules`` list."""
    if not isinstance(rule, dict):
        raise InvalidValidation(f"{rsrc_kind}.validations.rules: each rule must be a mapping")

    name = rule.get("name")
    if not name:
        raise InvalidValidation(f"{rsrc_kind}.validations.rules: every rule needs a 'name'")
    where = f"{rsrc_kind}.validations.rules['{name}']"
    _check_keys(where, rule, _RULE_KEYS)

    if not rule.get("expr"):
        raise InvalidValidation(f"{where}: an 'expr' is required, a CEL expression to evaluate")

    methods = rule.get("methods", list(DEFAULT_METHODS["expr"]))
    _check_methods(where, methods)

    refs = rule.get("refs") or {}
    if not isinstance(refs, dict):
        raise InvalidValidation(f"{where}: 'refs' must be a mapping of name to lookup")

    return {
        "name": name,
        "description": rule.get("description"),
        "resource": rsrc_kind,
        "kind": "expr",
        "field": None,
        "methods": list(methods),
        "refs": [_normalise_ref(where, ref_name, refs[ref_name], kinds) for ref_name in refs],
        "expr": rule["expr"],
        "error": _normalise_error(
            where, rule.get("error"), 422, f"Validation rule '{name}' failed."
        ),
        "examples": _normalise_examples(where, rule.get("examples")),
    }


def extract(rsrc_data: list) -> dict:
    """Extract the normalised rules for every resource that declares any.

    Resources that declare no ``references`` and no ``validations`` contribute
    nothing, so an unannotated project gets an empty result and every downstream
    generator behaves exactly as it did before.

    :param list rsrc_data: the resource data, as loaded from the resource files
    :return: a mapping of resource kind to its list of rules, kinds with no rules omitted
    :rtype: dict
    """
    kinds = {rsrc["kind"]: rsrc for rsrc in rsrc_data}
    ruleset = {}

    for rsrc in rsrc_data:
        rsrc_kind = rsrc["kind"]
        rules = []

        properties = rsrc.get("schema", {}).get("items", {}).get("properties", {})
        for prop in properties:
            prop_schema = properties[prop]
            if not isinstance(prop_schema, dict) or "references" not in prop_schema:
                continue
            rules.extend(_reference_rules(rsrc_kind, prop, prop_schema["references"], kinds))

        validations = rsrc.get("validations") or {}
        if not isinstance(validations, dict):
            raise InvalidValidation(f"{rsrc_kind}.validations: must be a mapping")
        _check_keys(f"{rsrc_kind}.validations", validations, {"rules"})

        for rule in validations.get("rules") or []:
            rules.append(_expr_rule(rsrc_kind, rule, kinds))

        names = [rule["name"] for rule in rules]
        dupes = sorted({name for name in names if names.count(name) > 1})
        if dupes:
            raise InvalidValidation(
                f"{rsrc_kind}: duplicate rule name(s) {', '.join(dupes)}; rule names must be "
                "unique within a resource"
            )

        if rules:
            _LOGGER.info(f"Extracted {len(rules)} validation rule(s) for {rsrc_kind}")
            ruleset[rsrc_kind] = rules

    return ruleset


def strip(rsrc_data: list) -> list:
    """Return a copy of the resource data with all validation keys removed.

    ``references`` and ``validations`` are firestone concepts, not JSON Schema, so
    they are taken out before the data reaches any generator.  This keeps them out
    of the OpenAPI components and out of the CLI, AsyncAPI and Streamlit output.

    :param list rsrc_data: the resource data, as loaded from the resource files
    :return: a deep copy with the validation keys removed
    :rtype: list
    """
    cleaned = copy.deepcopy(rsrc_data)
    for rsrc in cleaned:
        rsrc.pop("validations", None)
        properties = rsrc.get("schema", {}).get("items", {}).get("properties", {})
        for prop in properties:
            if isinstance(properties[prop], dict):
                properties[prop].pop("references", None)

    return cleaned


def methods_with_rules(rules: list) -> set:
    """Get the set of HTTP methods that at least one of ``rules`` runs on."""
    methods = set()
    for rule in rules:
        methods.update(rule["methods"])

    return methods


def problem_component() -> dict:
    """Get the RFC 9457 problem detail component returned when a rule fails."""
    return {
        "type": "object",
        "description": (
            "An RFC 9457 problem detail, returned when one or more validation rules fail."
        ),
        "properties": {
            "type": {"type": "string", "default": "about:blank"},
            "title": {"type": "string", "description": "A short summary of the problem."},
            "status": {"type": "integer", "description": "The HTTP status code."},
            "detail": {"type": "string", "description": "The first violation's message."},
            "violations": {
                "type": "array",
                "description": "Every rule that failed for this request.",
                "items": {
                    "type": "object",
                    "properties": {
                        "rule": {"type": "string", "description": "The name of the rule."},
                        "resource": {"type": "string", "description": "The resource validated."},
                        "field": {
                            "type": "string",
                            "description": "The field the rule applies to, if any.",
                        },
                        "message": {"type": "string", "description": "Why the rule failed."},
                    },
                    "required": ["rule", "resource", "message"],
                },
            },
        },
        "required": ["title", "status", "violations"],
    }


def openapi_extension(ruleset: dict) -> dict:
    """Get the rules as they are published in the OpenAPI document.

    A rule's examples are build time test data rather than part of the API
    contract, so they are left out, along with any field the rule does not use.

    :param dict ruleset: the rules, as returned by :func:`extract`
    :return: the same rules, trimmed down to what a reader of the spec needs
    :rtype: dict
    """
    published = {}
    for rsrc_kind in ruleset:
        published[rsrc_kind] = [
            {
                key: value
                for key, value in rule.items()
                if key != "examples" and value not in (None, [], {})
            }
            for rule in ruleset[rsrc_kind]
        ]

    return published


def problem_response(rules: list, method: str = None) -> dict:
    """Get the error responses to add to an operation covered by ``rules``.

    :param list rules: the rules for this resource
    :param str method: only describe what the rules running on this method can return
    """
    if method:
        rules = [rule for rule in rules if method in rule["methods"]]

    responses = {}
    for status in sorted({rule["error"]["status"] for rule in rules}):
        responses[status] = {
            "description": "One or more validation rules failed",
            "content": {
                "application/problem+json": {
                    "schema": {"$ref": f"#/components/schemas/{PROBLEM_COMPONENT}"},
                },
            },
        }

    return responses


def _string(value: str) -> str:
    """Quote a string the way black would, preferring double quotes."""
    if '"' in value and "'" not in value:
        return f"'{value}'"

    return json.dumps(value, ensure_ascii=False)


def _literal(data, indent: int = 1) -> str:
    """Format a value as a Python literal that black will leave alone.

    Every collection is written out one entry per line with a trailing comma,
    which is black's "magic trailing comma": it keeps the exploded form as is
    rather than reflowing it. That makes the generated rules diff cleanly and
    survive a formatting pass unchanged.
    """
    pad = "    " * indent
    closing = "    " * (indent - 1)

    if isinstance(data, dict):
        if not data:
            return "{}"
        entries = "\n".join(
            f"{pad}{_string(key)}: {_literal(data[key], indent + 1)}," for key in data
        )
        return "{\n" + entries + f"\n{closing}}}"

    if isinstance(data, (list, tuple)):
        if not data:
            return "[]"
        entries = "\n".join(f"{pad}{_literal(item, indent + 1)}," for item in data)
        return "[\n" + entries + f"\n{closing}]"

    if isinstance(data, str):
        return _string(data)

    return repr(data)


def _examples(ruleset: dict) -> list:
    """Flatten every rule's examples into the rows the generated test suite runs."""
    rows = []
    for rsrc in ruleset:
        for rule in ruleset[rsrc]:
            for example in rule["examples"]:
                rows.append((rsrc, rule["name"], rule["methods"][0], example))

    return rows


def _rust_string(value: str) -> str:
    """Quote a string as a Rust literal.

    Rust does not accept JSON's ``\\uXXXX`` escape, and a raw string cannot be used
    because the rules are JSON and may contain the closing delimiter, so the few
    characters that need escaping are handled directly.
    """
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    escaped = escaped.replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t")
    escaped = "".join(char if ord(char) >= 0x20 else f"\\u{{{ord(char):x}}}" for char in escaped)

    return f'"{escaped}"'


def _generate_python(ruleset: dict, examples: list, with_tests: bool) -> dict:
    """Generate the python validation package."""
    files = {}
    for name in ("__init__.py", "ports.py", "runtime.py"):
        tmpl = spec_base.JINJA_ENV.get_template(f"validations/python/{name}.jinja2")
        files[name] = tmpl.render()

    has_expr = any(rule["kind"] == "expr" for rules in ruleset.values() for rule in rules)
    tmpl = spec_base.JINJA_ENV.get_template("validations/python/rules.py.jinja2")
    files["rules.py"] = tmpl.render(rules_literal=_literal(ruleset), has_expr=has_expr)

    if with_tests and examples:
        tmpl = spec_base.JINJA_ENV.get_template("validations/python/test_rules.py.jinja2")
        files["test_rules.py"] = tmpl.render(examples_literal=_literal(examples))

    return files


def _generate_rust(ruleset: dict, examples: list, with_tests: bool) -> dict:
    """Generate the rust validation package.

    The rules are embedded as JSON and parsed once, rather than written out as a
    Rust literal: it keeps the generated source small, stable under rustfmt, and
    identical in meaning to what the python package carries.
    """
    has_expr = any(rule["kind"] == "expr" for rules in ruleset.values() for rule in rules)
    has_examples = bool(with_tests and examples)

    files = {}
    tmpl = spec_base.JINJA_ENV.get_template("validations/rust/ports.rs.jinja2")
    files["ports.rs"] = tmpl.render()

    tmpl = spec_base.JINJA_ENV.get_template("validations/rust/runtime.rs.jinja2")
    files["runtime.rs"] = tmpl.render()

    tmpl = spec_base.JINJA_ENV.get_template("validations/rust/rules.rs.jinja2")
    files["rules.rs"] = tmpl.render(
        rules_literal=_rust_string(json.dumps(ruleset)), has_expr=has_expr
    )

    tmpl = spec_base.JINJA_ENV.get_template("validations/rust/mod.rs.jinja2")
    files["mod.rs"] = tmpl.render(has_expr=has_expr, has_examples=has_examples)

    if has_examples:
        # The rust tests look their example up by index, so the rules stay the one
        # copy of the data rather than being written out twice.
        tmpl = spec_base.JINJA_ENV.get_template("validations/rust/tests.rs.jinja2")
        files["tests.rs"] = tmpl.render(
            examples_literal=_rust_string(json.dumps(_indexed(examples)))
        )

    return files


def _indexed(examples: list) -> list:
    """Number each rule's examples, so a test can find one without repeating it."""
    seen = {}
    rows = []
    for rsrc, name, method, _ in examples:
        index = seen.get((rsrc, name), 0)
        seen[(rsrc, name)] = index + 1
        rows.append((rsrc, name, method, index))

    return rows


def generate(ruleset: dict, language: str = LANG_PYTHON, with_tests: bool = True) -> dict:
    """Generate a self-contained validation package for the given rules.

    The generated package has no runtime dependency on firestone.  A CEL runtime
    is only needed by a rule that carries an expression, so a project using
    nothing but ``references`` needs no extra dependency at all.

    :param dict ruleset: the rules, as returned by :func:`extract`
    :param str language: the language to generate for, one of :data:`LANGUAGES`
    :param bool with_tests: also generate a test suite from the rules' examples
    :return: a mapping of file name to file contents
    :rtype: dict
    """
    if language not in LANGUAGES:
        raise InvalidValidation(
            f"Cannot generate validations for '{language}', only {', '.join(LANGUAGES)}"
        )

    examples = _examples(ruleset)
    if language == LANG_RUST:
        files = _generate_rust(ruleset, examples, with_tests)
    else:
        files = _generate_python(ruleset, examples, with_tests)

    return {name: content.rstrip("\n") + "\n" for name, content in files.items()}
