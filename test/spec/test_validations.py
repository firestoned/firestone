# pylint: disable=too-many-lines
# pylint: disable=duplicate-code
"""
Test the firestone.spec.validations module, and the package it generates.
"""

import asyncio
import copy
import importlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

import pytest
import yaml

from firestone.spec import openapi
from firestone.spec import validations


def _resource(kind: str = "addressbook", **extra) -> dict:
    """Get a minimal resource, with anything extra merged over it."""
    rsrc = {
        "kind": kind,
        "apiVersion": "v1",
        "methods": {"resource": ["get", "post"], "instance": ["get", "put", "patch", "delete"]},
        "schema": {
            "type": "array",
            "key": {"name": f"{kind}_key", "schema": {"type": "string"}},
            "items": {
                "type": "object",
                "properties": {
                    "person": {"type": "object"},
                    "city": {"type": "string"},
                    "is_valid": {"type": "boolean"},
                },
            },
        },
    }
    rsrc.update(extra)

    return rsrc


def _with_reference(reference: dict, kind: str = "addressbook") -> dict:
    """Get a resource whose 'person' property carries the given references block."""
    rsrc = _resource(kind)
    rsrc["schema"]["items"]["properties"]["person"]["references"] = reference

    return rsrc


def _referencing(reference: dict) -> list:
    """Get a resource carrying the given reference, alongside the resource it points at.

    Firestone needs the target to work out the key to match on, so the two travel
    together unless a test is specifically about a target it was not given.
    """
    return [_with_reference(reference), _resource(reference.get("kind", "persons"))]


def _with_rule(rule: dict, kind: str = "addressbook") -> dict:
    """Get a resource carrying the given validation rule."""
    return _resource(kind, validations={"rules": [rule]})


class TestExtractReferences(unittest.TestCase):
    """Test firestone.spec.validations.extract() for property level references."""

    def test_no_validations(self):
        """A resource that declares nothing contributes nothing."""
        self.assertEqual(validations.extract([_resource()]), {})

    def test_exists_rule(self):
        """A reference becomes an existence rule."""
        ruleset = validations.extract(
            _referencing({"kind": "persons", "key": "first_name", "value": "person.name"})
        )

        self.assertIn("addressbook", ruleset)
        self.assertEqual(len(ruleset["addressbook"]), 1)

        rule = ruleset["addressbook"][0]
        self.assertEqual(rule["name"], "person_must_exist")
        self.assertEqual(rule["kind"], "exists")
        self.assertEqual(rule["field"], "person.name")
        self.assertEqual(rule["methods"], ["post", "put", "patch"])
        self.assertEqual(rule["error"]["status"], 422)
        self.assertEqual(
            rule["refs"],
            [
                {
                    "name": "person",
                    "kind": "persons",
                    "key": "first_name",
                    "value": "person.name",
                    "optional": False,
                }
            ],
        )

    def test_value_defaults_to_the_property(self):
        """A reference with no 'value' looks the property itself up."""
        ruleset = validations.extract(_referencing({"kind": "persons", "key": "name"}))

        self.assertEqual(ruleset["addressbook"][0]["refs"][0]["value"], "person")

    def test_key_defaults_to_the_target_schema_key(self):
        """A reference with no 'key' matches on the referenced resource's key."""
        ruleset = validations.extract(
            [
                _with_reference({"kind": "persons", "value": "person.uuid"}),
                _resource("persons"),
            ]
        )

        self.assertEqual(ruleset["addressbook"][0]["refs"][0]["key"], "persons_key")

    def test_unknown_kind_without_a_key(self):
        """A key firestone cannot work out has to be given, not guessed at."""
        with self.assertRaises(validations.InvalidValidation) as ctx:
            validations.extract([_with_reference({"kind": "elsewhere"})])

        self.assertIn("not one of the resources given to firestone", str(ctx.exception))

    def test_unknown_kind_with_a_key(self):
        """A resource generated elsewhere is fine once it says what to match on."""
        ruleset = validations.extract(
            _referencing({"kind": "elsewhere", "key": "name", "value": "person.name"})
        )

        self.assertEqual(ruleset["addressbook"][0]["refs"][0]["key"], "name")

    def test_target_without_a_schema_key(self):
        """A target with no key of its own has to be pointed at explicitly."""
        target = _resource("persons")
        del target["schema"]["key"]

        with self.assertRaises(validations.InvalidValidation) as ctx:
            validations.extract([_with_reference({"kind": "persons"}), target])

        self.assertIn("has no schema key", str(ctx.exception))

    def test_on_missing_ignore(self):
        """A reference that tolerates a missing target produces no existence rule."""
        ruleset = validations.extract(_referencing({"kind": "persons", "on_missing": "ignore"}))

        self.assertEqual(ruleset, {})

    def test_immutable(self):
        """An immutable reference adds a rule on the updating methods."""
        ruleset = validations.extract(_referencing({"kind": "persons", "immutable": True}))

        self.assertEqual([rule["kind"] for rule in ruleset["addressbook"]], ["exists", "immutable"])

        rule = ruleset["addressbook"][1]
        self.assertEqual(rule["name"], "person_is_immutable")
        self.assertEqual(rule["methods"], ["put", "patch"])
        self.assertEqual(rule["error"]["status"], 409)

    def test_missing_kind(self):
        """A reference has to say what it references."""
        with self.assertRaises(validations.InvalidValidation) as ctx:
            validations.extract(_referencing({"key": "name"}))

        self.assertIn("a 'kind' is required", str(ctx.exception))

    def test_unknown_key(self):
        """A typo in a reference is reported rather than ignored."""
        with self.assertRaises(validations.InvalidValidation) as ctx:
            validations.extract(_referencing({"kind": "persons", "immutible": True}))

        self.assertIn("unknown key(s) immutible", str(ctx.exception))

    def test_bad_on_missing(self):
        """on_missing only takes the two values it documents."""
        with self.assertRaises(validations.InvalidValidation) as ctx:
            validations.extract(_referencing({"kind": "persons", "on_missing": "maybe"}))

        self.assertIn("on_missing must be", str(ctx.exception))


class TestExtractRules(unittest.TestCase):
    """Test firestone.spec.validations.extract() for top level validation rules."""

    def test_defaults(self):
        """A rule with only a name and an expression gets sensible defaults."""
        ruleset = validations.extract([_with_rule({"name": "always", "expr": "true"})])

        rule = ruleset["addressbook"][0]
        self.assertEqual(rule["kind"], "expr")
        self.assertEqual(rule["methods"], ["post", "put", "patch"])
        self.assertEqual(rule["refs"], [])
        self.assertEqual(
            rule["error"], {"status": 422, "message": "Validation rule 'always' failed."}
        )

    def test_refs(self):
        """A rule's refs are normalised into the generated form."""
        ruleset = validations.extract(
            [
                _with_rule(
                    {
                        "name": "matches",
                        "methods": ["post"],
                        "refs": {"postal": {"kind": "postal_codes", "value": "postal_code"}},
                        "expr": "refs.postal.city == self.city",
                        "error": {"status": 409, "message": "no"},
                    }
                ),
                _resource("postal_codes"),
            ]
        )

        rule = ruleset["addressbook"][0]
        self.assertEqual(
            rule["refs"],
            [
                {
                    "name": "postal",
                    "kind": "postal_codes",
                    "key": "postal_codes_key",
                    "value": "postal_code",
                    "optional": False,
                }
            ],
        )
        self.assertEqual(rule["error"], {"status": 409, "message": "no"})

    def test_missing_name(self):
        """Every rule needs a name, so that violations can be traced back to it."""
        with self.assertRaises(validations.InvalidValidation) as ctx:
            validations.extract([_with_rule({"expr": "true"})])

        self.assertIn("every rule needs a 'name'", str(ctx.exception))

    def test_missing_expr(self):
        """A rule with no expression has nothing to evaluate."""
        with self.assertRaises(validations.InvalidValidation) as ctx:
            validations.extract([_with_rule({"name": "nope"})])

        self.assertIn("an 'expr' is required", str(ctx.exception))

    def test_non_mutating_method(self):
        """Rules cannot be attached to reads."""
        with self.assertRaises(validations.InvalidValidation) as ctx:
            validations.extract([_with_rule({"name": "r", "expr": "true", "methods": ["get"]})])

        self.assertIn("cannot validate on get", str(ctx.exception))

    def test_empty_methods(self):
        """A rule that runs on nothing is a mistake, not a no-op."""
        with self.assertRaises(validations.InvalidValidation) as ctx:
            validations.extract([_with_rule({"name": "r", "expr": "true", "methods": []})])

        self.assertIn("must be a non-empty list", str(ctx.exception))

    def test_bad_status(self):
        """An error status has to be one a client could act on."""
        with self.assertRaises(validations.InvalidValidation) as ctx:
            validations.extract(
                [_with_rule({"name": "r", "expr": "true", "error": {"status": 200}})]
            )

        self.assertIn("is not a 4xx or 5xx", str(ctx.exception))

    def test_optional_ref(self):
        """A rule about absence marks its lookup optional."""
        ruleset = validations.extract(
            [
                _with_rule(
                    {
                        "name": "r",
                        "expr": "!has(refs.p)",
                        "refs": {
                            "p": {"kind": "persons", "key": "name", "value": "a", "optional": True}
                        },
                    }
                )
            ]
        )

        self.assertTrue(ruleset["addressbook"][0]["refs"][0]["optional"])

    def test_bad_optional(self):
        """'optional' is a flag, not a string."""
        with self.assertRaises(validations.InvalidValidation) as ctx:
            validations.extract(
                [
                    _with_rule(
                        {
                            "name": "r",
                            "expr": "true",
                            "refs": {
                                "p": {
                                    "kind": "persons",
                                    "key": "n",
                                    "value": "a",
                                    "optional": "yes",
                                }
                            },
                        }
                    )
                ]
            )

        self.assertIn("must be true or false", str(ctx.exception))

    def test_ref_without_value(self):
        """A ref has to say where in the body its lookup value comes from."""
        with self.assertRaises(validations.InvalidValidation) as ctx:
            validations.extract(
                [_with_rule({"name": "r", "expr": "true", "refs": {"p": {"kind": "persons"}}})]
            )

        self.assertIn("a 'value' is required", str(ctx.exception))

    def test_ref_name_must_be_an_identifier(self):
        """A ref name has to be usable in an expression."""
        with self.assertRaises(validations.InvalidValidation) as ctx:
            validations.extract(
                [
                    _with_rule(
                        {
                            "name": "r",
                            "expr": "true",
                            "refs": {"my ref": {"kind": "persons", "value": "a"}},
                        }
                    )
                ]
            )

        self.assertIn("must be a valid identifier", str(ctx.exception))

    def test_duplicate_names(self):
        """Two rules with one name would make violations ambiguous."""
        rsrc = _resource(
            validations={
                "rules": [{"name": "same", "expr": "true"}, {"name": "same", "expr": "false"}]
            }
        )

        with self.assertRaises(validations.InvalidValidation) as ctx:
            validations.extract([rsrc])

        self.assertIn("duplicate rule name(s) same", str(ctx.exception))

    def test_reference_and_rule_name_collide(self):
        """A hand written rule cannot shadow one desugared from a reference."""
        rsrc = _with_reference({"kind": "persons"})
        rsrc["validations"] = {"rules": [{"name": "person_must_exist", "expr": "true"}]}

        with self.assertRaises(validations.InvalidValidation) as ctx:
            validations.extract([rsrc, _resource("persons")])

        self.assertIn("duplicate rule name(s) person_must_exist", str(ctx.exception))

    def test_bad_expect(self):
        """An example has to say whether it should be accepted or rejected."""
        with self.assertRaises(validations.InvalidValidation) as ctx:
            validations.extract(
                [_with_rule({"name": "r", "expr": "true", "examples": [{"self": {}}]})]
            )

        self.assertIn("'expect' must be 'pass' or 'fail'", str(ctx.exception))

    def test_examples_are_normalised(self):
        """An example gets every scope filled in, so the generated tests are uniform."""
        ruleset = validations.extract(
            [_with_rule({"name": "r", "expr": "true", "examples": [{"expect": "pass"}]})]
        )

        self.assertEqual(
            ruleset["addressbook"][0]["examples"],
            [{"self": {}, "old": None, "refs": {}, "ctx": {}, "expect": "pass"}],
        )


class TestStrip(unittest.TestCase):
    """Test firestone.spec.validations.strip()"""

    def test_removes_both_kinds(self):
        """Validation keys never reach a generator."""
        rsrc = _with_reference({"kind": "persons"})
        rsrc["validations"] = {"rules": [{"name": "r", "expr": "true"}]}

        cleaned = validations.strip([rsrc])[0]

        self.assertNotIn("validations", cleaned)
        self.assertNotIn("references", cleaned["schema"]["items"]["properties"]["person"])

    def test_does_not_mutate(self):
        """The caller's data is left alone."""
        rsrc = _with_reference({"kind": "persons"})
        before = copy.deepcopy(rsrc)

        validations.strip([rsrc])

        self.assertEqual(rsrc, before)

    def test_leaves_plain_resources_alone(self):
        """A resource with no validations comes back unchanged."""
        rsrc = _resource()

        self.assertEqual(validations.strip([rsrc]), [rsrc])


class TestHelpers(unittest.TestCase):
    """Test the smaller helpers of firestone.spec.validations."""

    def test_methods_with_rules(self):
        """The methods are the union of every rule's."""
        rules = [{"methods": ["post"]}, {"methods": ["put", "patch"]}]

        self.assertEqual(validations.methods_with_rules(rules), {"post", "put", "patch"})

    def test_problem_response(self):
        """One response per distinct status the rules can return."""
        rules = [{"error": {"status": 422}}, {"error": {"status": 403}}, {"error": {"status": 422}}]
        responses = validations.problem_response(rules)

        self.assertEqual(sorted(responses), [403, 422])
        self.assertEqual(
            responses[422]["content"]["application/problem+json"]["schema"],
            {"$ref": f"#/components/schemas/{validations.PROBLEM_COMPONENT}"},
        )

    def test_problem_component(self):
        """The problem component describes every violation."""
        component = validations.problem_component()

        self.assertIn("violations", component["properties"])
        self.assertEqual(component["properties"]["status"]["type"], "integer")


class TestGenerate(unittest.TestCase):
    """Test firestone.spec.validations.generate()"""

    def test_files(self):
        """The engine, the interfaces and the rules are always generated."""
        ruleset = validations.extract(_referencing({"kind": "persons"}))
        files = validations.generate(ruleset)

        self.assertEqual(sorted(files), ["__init__.py", "ports.py", "rules.py", "runtime.py"])
        self.assertIn("person_must_exist", files["rules.py"])

    def test_no_tests_without_examples(self):
        """Rules with no examples produce no test file."""
        ruleset = validations.extract([_with_rule({"name": "r", "expr": "true"})])

        self.assertNotIn("test_rules.py", validations.generate(ruleset))

    def test_tests_from_examples(self):
        """Rules with examples produce a test file."""
        ruleset = validations.extract(
            [_with_rule({"name": "r", "expr": "true", "examples": [{"expect": "pass"}]})]
        )

        self.assertIn("test_rules.py", validations.generate(ruleset))

    def test_tests_can_be_turned_off(self):
        """The generated test suite is optional."""
        ruleset = validations.extract(
            [_with_rule({"name": "r", "expr": "true", "examples": [{"expect": "pass"}]})]
        )

        self.assertNotIn("test_rules.py", validations.generate(ruleset, with_tests=False))

    def test_cel_note_only_when_needed(self):
        """A project using only references is told nothing about CEL."""
        references = validations.generate(validations.extract(_referencing({"kind": "p"})))
        expressions = validations.generate(
            validations.extract([_with_rule({"name": "r", "expr": "true"})])
        )

        self.assertNotIn("cel-python", references["rules.py"])
        self.assertIn("cel-python", expressions["rules.py"])

    def test_generated_code_is_black_formatted(self):
        """Generated code survives a formatting pass unchanged.

        It lands in the consumer's repository, so it has to look like code
        somebody wrote, and it must not churn every time it is regenerated.
        """
        black = pytest.importorskip("black")
        mode = black.Mode(line_length=100)
        ruleset = validations.extract(
            [
                _with_rule(
                    {
                        "name": "quoting",
                        "expr": 'has(ctx.roles) && "admin" in ctx.roles',
                        "examples": [{"self": {"a": 1}, "expect": "fail"}],
                    }
                )
            ]
        )

        for name, content in validations.generate(ruleset).items():
            self.assertEqual(
                black.format_str(content, mode=mode), content, f"{name} is unformatted"
            )

    def test_generation_is_idempotent(self):
        """Regenerating without changing a schema changes nothing."""
        ruleset = validations.extract([_with_rule({"name": "r", "expr": "true"})])

        self.assertEqual(validations.generate(ruleset), validations.generate(ruleset))

    def test_generated_code_is_valid_python(self):
        """Everything generated compiles."""
        ruleset = validations.extract(
            [_with_rule({"name": "r", "expr": "true", "examples": [{"expect": "pass"}]})]
        )

        for name, content in validations.generate(ruleset).items():
            compile(content, name, "exec")


class TestGenerateRust(unittest.TestCase):
    """Test firestone.spec.validations.generate() for the rust target."""

    def _ruleset(self):
        return validations.extract(
            [
                _with_rule(
                    {
                        "name": "r",
                        "expr": 'has(ctx.roles) && "admin" in ctx.roles',
                        "examples": [{"self": {"a": 1}, "expect": "fail"}],
                    }
                )
            ]
        )

    def test_files(self):
        """A rust package is a module tree, not a python one."""
        files = validations.generate(self._ruleset(), language="rust")

        self.assertEqual(
            sorted(files), ["mod.rs", "ports.rs", "rules.rs", "runtime.rs", "tests.rs"]
        )

    @staticmethod
    def _embedded(files: dict, name: str, const: str):
        """Decode a generated rust string literal back to the value it carries.

        A rust literal using only the escapes firestone emits is also valid JSON
        string syntax, so it decodes without needing a rust toolchain.
        """
        literal = files[name].split(f"const {const}: &str = ")[1].split(";\n")[0]

        return json.loads(json.loads(literal))

    def test_rules_are_embedded_as_json(self):
        """The rules travel as JSON, so both languages carry the same data."""
        files = validations.generate(self._ruleset(), language="rust")

        self.assertEqual(self._embedded(files, "rules.rs", "RULES_JSON"), self._ruleset())

    def test_examples_are_addressed_by_index(self):
        """The rust tests point back at the rules rather than duplicating them."""
        files = validations.generate(self._ruleset(), language="rust")

        self.assertEqual(
            self._embedded(files, "tests.rs", "EXAMPLES"), [["addressbook", "r", "post", 0]]
        )

    def test_no_tests_without_examples(self):
        """A rust package with no examples declares no test module."""
        ruleset = validations.extract([_with_rule({"name": "r", "expr": "true"})])
        files = validations.generate(ruleset, language="rust")

        self.assertNotIn("tests.rs", files)
        self.assertNotIn("mod tests;", files["mod.rs"])

    def test_tests_can_be_turned_off(self):
        """--no-tests works the same for both languages."""
        files = validations.generate(self._ruleset(), language="rust", with_tests=False)

        self.assertNotIn("tests.rs", files)

    def test_cel_dependency_only_when_needed(self):
        """A project using only references is not told to add a CEL runtime."""
        references = validations.generate(
            validations.extract(_referencing({"kind": "persons"})), language="rust"
        )
        expressions = validations.generate(self._ruleset(), language="rust")

        self.assertNotIn("cel-interpreter", references["mod.rs"])
        self.assertIn("cel-interpreter", expressions["mod.rs"])

    def test_expression_quoting_survives(self):
        """An expression carrying quotes comes back out of the literal intact."""
        files = validations.generate(self._ruleset(), language="rust")
        rule = self._embedded(files, "rules.rs", "RULES_JSON")["addressbook"][0]

        self.assertEqual(rule["expr"], 'has(ctx.roles) && "admin" in ctx.roles')

    def test_unknown_language(self):
        """An unsupported target is refused with a useful message."""
        with self.assertRaises(validations.InvalidValidation) as ctx:
            validations.generate({}, language="cobol")

        self.assertIn("only python, rust", str(ctx.exception))

    def test_generation_is_idempotent(self):
        """Regenerating without changing a schema changes nothing."""
        ruleset = self._ruleset()

        self.assertEqual(
            validations.generate(ruleset, language="rust"),
            validations.generate(ruleset, language="rust"),
        )

    def test_generated_code_is_rustfmt_formatted(self):
        """Generated rust survives a formatting pass unchanged.

        Skipped where there is no toolchain; CI for firestone is python only.
        """
        if shutil.which("rustfmt") is None:
            self.skipTest("rustfmt is not installed")

        for name, content in validations.generate(self._ruleset(), language="rust").items():
            result = subprocess.run(
                ["rustfmt", "--edition", "2021", "--emit", "stdout", "--quiet"],
                input=content,
                capture_output=True,
                text=True,
                check=True,
            )
            self.assertEqual(result.stdout, content, f"{name} is unformatted")


class TestOpenAPIIntegration(unittest.TestCase):
    """Test how validations show up in the generated OpenAPI document."""

    def _generate(self, rsrc_data):
        return openapi.generate(rsrc_data, "title", "desc", "summary", "1.0")

    def test_unannotated_spec_is_untouched(self):
        """A project with no validations gets no extension and no new component."""
        spec = self._generate([_resource()])

        self.assertNotIn(validations.OPENAPI_EXTENSION, spec)
        self.assertNotIn(validations.PROBLEM_COMPONENT, spec)

    def test_extension_is_emitted(self):
        """The rules ride along in the document as a vendor extension."""
        spec = self._generate(_referencing({"kind": "persons", "value": "person.name"}))

        self.assertIn(validations.OPENAPI_EXTENSION, spec)
        self.assertIn("person_must_exist", spec)

    def test_problem_component_is_added(self):
        """The error shape is described once, in components."""
        spec = self._generate(_referencing({"kind": "persons"}))

        self.assertIn(validations.PROBLEM_COMPONENT, spec)

    def test_references_are_stripped_from_components(self):
        """A firestone concept never leaks into a JSON Schema component."""
        spec = self._generate(_referencing({"kind": "persons"}))

        self.assertNotIn("references:", spec)

    def test_error_response_on_covered_methods(self):
        """Only the operations the rules run on gain an error response."""
        rsrc = _with_rule(
            {"name": "r", "expr": "true", "methods": ["post"], "error": {"status": 409}}
        )
        paths = yaml.safe_load(self._generate([rsrc]))["paths"]

        self.assertIn(409, paths["/addressbook"]["post"]["responses"])
        self.assertNotIn(409, paths["/addressbook"]["get"]["responses"])
        self.assertNotIn(409, paths["/addressbook/{addressbook_key}"]["put"]["responses"])

    def test_error_response_on_the_instance_path(self):
        """An updating rule covers the instance operations too."""
        rsrc = _with_rule({"name": "r", "expr": "true", "methods": ["put"]})
        paths = yaml.safe_load(self._generate([rsrc]))["paths"]

        self.assertIn(422, paths["/addressbook/{addressbook_key}"]["put"]["responses"])
        self.assertNotIn(422, paths["/addressbook"]["post"]["responses"])

    def test_error_response_content_type(self):
        """Validation failures are served as an RFC 9457 problem document."""
        rsrc = _with_rule({"name": "r", "expr": "true", "methods": ["post"]})
        spec = yaml.safe_load(self._generate([rsrc]))
        response = spec["paths"]["/addressbook"]["post"]["responses"][422]

        self.assertEqual(
            response["content"]["application/problem+json"]["schema"]["$ref"],
            f"#/components/schemas/{validations.PROBLEM_COMPONENT}",
        )
        self.assertIn(validations.PROBLEM_COMPONENT, spec["components"]["schemas"])

    def test_successful_responses_are_kept(self):
        """Adding an error response does not displace the ones already there."""
        rsrc = _with_rule({"name": "r", "expr": "true", "methods": ["post"]})
        paths = yaml.safe_load(self._generate([rsrc]))["paths"]

        self.assertIn(201, paths["/addressbook"]["post"]["responses"])

    def test_response_is_scoped_to_the_method(self):
        """An operation only advertises what its own rules can return."""
        rsrc = _resource(
            validations={
                "rules": [
                    {"name": "a", "expr": "true", "methods": ["post"], "error": {"status": 422}},
                    {"name": "b", "expr": "true", "methods": ["patch"], "error": {"status": 403}},
                ]
            }
        )
        paths = yaml.safe_load(self._generate([rsrc]))["paths"]

        self.assertEqual(sorted(paths["/addressbook"]["post"]["responses"]), [201, 422])
        self.assertEqual(
            sorted(paths["/addressbook/{addressbook_key}"]["patch"]["responses"]), [200, 403]
        )

    def test_examples_are_not_published(self):
        """Test data for the rules stays out of the API contract."""
        rsrc = _with_rule({"name": "r", "expr": "true", "examples": [{"expect": "pass"}]})
        spec = yaml.safe_load(self._generate([rsrc]))
        rule = spec[validations.OPENAPI_EXTENSION]["addressbook"][0]

        self.assertNotIn("examples", rule)
        self.assertNotIn("refs", rule)
        self.assertEqual(rule["name"], "r")

    def test_attribute_routes_are_covered(self):
        """Updating one attribute can break a rule, so those routes say so too."""
        rsrc = _with_rule({"name": "r", "expr": "true", "methods": ["put"]})
        rsrc["methods"]["instance_attrs"] = ["get", "put"]
        paths = yaml.safe_load(self._generate([rsrc]))["paths"]

        self.assertIn(422, paths["/addressbook/{addressbook_key}/city"]["put"]["responses"])
        self.assertNotIn(422, paths["/addressbook/{addressbook_key}/city"]["get"]["responses"])

    def test_attribute_routes_without_rules_are_untouched(self):
        """A resource with no rules gains nothing on its attribute routes."""
        rsrc = _resource()
        rsrc["methods"]["instance_attrs"] = ["get", "put"]
        paths = yaml.safe_load(self._generate([rsrc]))["paths"]

        self.assertEqual(
            sorted(paths["/addressbook/{addressbook_key}/city"]["put"]["responses"]), [200]
        )

    def test_validations_can_be_suppressed(self):
        """Passing an empty ruleset leaves validations out entirely."""
        spec = openapi.generate(
            _referencing({"kind": "persons"}),
            "title",
            "desc",
            "summary",
            "1.0",
            validations={},
        )

        self.assertNotIn(validations.OPENAPI_EXTENSION, spec)


# pylint: disable=too-many-public-methods
class TestGeneratedRuntime(unittest.TestCase):
    """Test the behaviour of the package firestone generates."""

    @classmethod
    def setUpClass(cls):
        """Generate a validation package and import it."""
        cls.tmpdir = tempfile.mkdtemp()
        rsrc = _with_reference({"kind": "persons", "key": "name", "value": "person.name"})
        rsrc["validations"] = {
            "rules": [
                {
                    "name": "only_admins_may_invalidate",
                    "methods": ["patch"],
                    "expr": 'self.is_valid == old.is_valid || "admin" in ctx.roles',
                    "error": {"status": 403, "message": "not allowed"},
                },
                {
                    "name": "city_matches",
                    "methods": ["post"],
                    "refs": {"postal": {"kind": "postal_codes", "key": "name", "value": "postal"}},
                    "expr": "refs.postal.city == self.city",
                    "error": {"message": "{self.postal} is not in {self.city}"},
                },
                {
                    "name": "not_in_use",
                    "methods": ["delete"],
                    "refs": {
                        "postal": {
                            "kind": "postal_codes",
                            "key": "name",
                            "value": "postal",
                            "optional": True,
                        }
                    },
                    "expr": "!has(refs.postal)",
                    "error": {"status": 409, "message": "still in use"},
                },
            ]
        }
        rsrc["schema"]["items"]["properties"]["person"]["references"]["immutable"] = True

        files = validations.generate(validations.extract([rsrc]))
        package = os.path.join(cls.tmpdir, "genval")
        os.makedirs(package)
        for name, content in files.items():
            with open(os.path.join(package, name), "w", encoding="utf-8") as fh:
                fh.write(content)

        sys.path.insert(0, cls.tmpdir)
        cls.genval = importlib.import_module("genval")

    @classmethod
    def tearDownClass(cls):
        sys.path.remove(cls.tmpdir)
        for name in [mod for mod in sys.modules if mod.startswith("genval")]:
            del sys.modules[name]
        shutil.rmtree(cls.tmpdir)

    def setUp(self):
        self.people = {"Ann": {"name": "Ann"}}
        self.codes = {"K1A": {"name": "K1A", "city": "Ottawa"}}
        self.requests = []
        self.contexts = []
        test = self

        # pylint: disable=too-few-public-methods
        class Resolver:
            """An in-memory stand-in for a database."""

            async def resolve(self, requests, ctx):
                """Look the requested resources up in the in-memory tables."""
                test.requests.extend(requests)
                test.contexts.append(ctx)
                found = {}
                for request in requests:
                    table = test.people if request.kind == "persons" else test.codes
                    if request.value in table:
                        found[request.id] = table[request.value]

                return found

        self.resolver = Resolver()

    def _validate(self, op, body=None, old=None, ctx=None):
        return asyncio.run(
            self.genval.validate(
                op, "addressbook", body=body, old=old, resolver=self.resolver, ctx=ctx
            )
        )

    def test_reference_found(self):
        """A body pointing at a resource that exists is accepted."""
        self._validate("post", {"person": {"name": "Ann"}, "postal": "K1A", "city": "Ottawa"})

    def test_reference_missing(self):
        """A body pointing at a resource that does not exist is rejected."""
        with self.assertRaises(self.genval.ValidationError) as ctx:
            self._validate("post", {"person": {"name": "Bob"}})

        error = ctx.exception
        self.assertEqual(error.status, 422)
        self.assertEqual(error.violations[0].rule, "person_must_exist")
        self.assertIn("Bob", error.violations[0].message)

    def test_problem_document(self):
        """A failure renders as an RFC 9457 problem document."""
        with self.assertRaises(self.genval.ValidationError) as ctx:
            self._validate("post", {"person": {"name": "Bob"}})

        problem = ctx.exception.to_problem()
        self.assertEqual(problem["status"], 422)
        self.assertEqual(problem["title"], "Validation failed")
        self.assertEqual(len(problem["violations"]), 1)
        self.assertEqual(problem["violations"][0]["field"], "person.name")

    def test_every_violation_is_reported(self):
        """A request that breaks two rules is told about both."""
        with self.assertRaises(self.genval.ValidationError) as ctx:
            self._validate("post", {"person": {"name": "Bob"}, "postal": "K1A", "city": "Toronto"})

        self.assertEqual(
            sorted(violation.rule for violation in ctx.exception.violations),
            ["city_matches", "person_must_exist"],
        )

    def test_status_is_the_highest(self):
        """The response status covers the most serious violation."""
        with self.assertRaises(self.genval.ValidationError) as ctx:
            self._validate("post", {"person": {"name": "Bob"}, "postal": "K1A", "city": "Toronto"})

        self.assertEqual(ctx.exception.status, 422)

    def test_message_interpolation(self):
        """An error message can quote the values that made it fail."""
        with self.assertRaises(self.genval.ValidationError) as ctx:
            self._validate("post", {"person": {"name": "Ann"}, "postal": "K1A", "city": "Toronto"})

        self.assertEqual(ctx.exception.violations[0].message, "K1A is not in Toronto")

    def test_lookups_are_batched(self):
        """Every lookup a request needs is asked for in one call."""
        self.people["Bob"] = {"name": "Bob"}
        self._validate("post", {"person": {"name": "Bob"}, "postal": "K1A", "city": "Ottawa"})

        self.assertEqual(len(self.requests), 2)

    def test_lookups_are_deduplicated(self):
        """Two rules wanting the same resource cost one lookup."""
        self._validate("post", {"person": {"name": "Ann"}, "postal": "K1A", "city": "Ottawa"})
        ids = [request.id for request in self.requests]

        self.assertEqual(len(ids), len(set(ids)))

    def test_unaffected_method(self):
        """A method no rule runs on needs no resolver at all."""
        asyncio.run(self.genval.validate("get", "addressbook", {"person": {"name": "Bob"}}))

    def test_unknown_resource(self):
        """A resource with no rules is a no-op."""
        asyncio.run(self.genval.validate("post", "not_a_resource", {"anything": True}))

    def test_patch_leaving_the_reference_alone(self):
        """An update that does not touch a reference does not look it up."""
        self._validate(
            "patch",
            {"city": "Toronto"},
            old={"person": {"name": "Ann"}, "is_valid": True},
            ctx={"roles": []},
        )

        self.assertEqual(self.requests, [])

    def test_patch_is_validated_against_the_merged_state(self):
        """A partial body is validated as the resource will end up."""
        with self.assertRaises(self.genval.ValidationError) as ctx:
            self._validate(
                "patch",
                {"person": {"name": "Bob"}},
                old={"person": {"name": "Ann"}, "is_valid": True},
                ctx={"roles": []},
            )

        self.assertEqual(
            sorted(violation.rule for violation in ctx.exception.violations),
            ["person_is_immutable", "person_must_exist"],
        )

    def test_immutable_allows_an_unchanged_value(self):
        """Resending the same reference is not a change."""
        self._validate(
            "patch",
            {"person": {"name": "Ann"}, "city": "Ottawa"},
            old={"person": {"name": "Ann"}, "is_valid": True},
            ctx={"roles": []},
        )

    def test_expression_reading_old_and_ctx(self):
        """A rule can compare against the current state and the caller."""
        with self.assertRaises(self.genval.ValidationError) as ctx:
            self._validate(
                "patch",
                {"is_valid": False},
                old={"person": {"name": "Ann"}, "is_valid": True},
                ctx={"roles": ["user"]},
            )

        self.assertEqual(ctx.exception.violations[0].rule, "only_admins_may_invalidate")
        self.assertEqual(ctx.exception.status, 403)

    def test_expression_passing_on_ctx(self):
        """The same rule accepts the change for a caller who is allowed to make it."""
        self._validate(
            "patch",
            {"is_valid": False},
            old={"person": {"name": "Ann"}, "is_valid": True},
            ctx={"roles": ["admin"]},
        )

    def test_pydantic_style_body(self):
        """A model with model_dump, as FastAPI hands over, is accepted."""

        # pylint: disable=too-few-public-methods
        class Body:
            """Stands in for a pydantic model."""

            def model_dump(self, mode=None, exclude_unset=None):
                """Get the model as a dict, the way pydantic does."""
                del mode, exclude_unset
                return {"person": {"name": "Ann"}}

        self._validate("post", Body())

    def test_missing_resolver(self):
        """Needing a lookup with no resolver is a bug, not a validation failure."""
        with self.assertRaises(self.genval.RuleEvaluationError):
            asyncio.run(self.genval.validate("post", "addressbook", {"person": {"name": "Ann"}}))

    def test_patch_merges_nested_objects(self):
        """A body touching one field of an embedded object keeps the rest of it."""
        runtime = importlib.import_module("genval.runtime")
        subject = runtime._subject(  # pylint: disable=protected-access
            "patch",
            {"person": {"name": "Ann"}},
            {"person": {"name": "Ann", "uuid": "u1"}, "city": "Ottawa"},
        )

        self.assertEqual(subject["person"], {"name": "Ann", "uuid": "u1"})
        self.assertEqual(subject["city"], "Ottawa")

    def test_patch_replaces_lists_outright(self):
        """A list is replaced rather than merged, as JSON Merge Patch has it."""
        runtime = importlib.import_module("genval.runtime")
        subject = runtime._subject(  # pylint: disable=protected-access
            "patch", {"hobbies": ["chess"]}, {"hobbies": ["golf", "sailing"]}
        )

        self.assertEqual(subject["hobbies"], ["chess"])

    def test_immutable_survives_a_nested_partial_update(self):
        """Updating a sibling field does not read as changing the reference.

        The reference is 'person.name'; a PATCH that only sets person.age must not
        look like the reference disappearing.
        """
        self._validate(
            "patch",
            {"person": {"age": 41}},
            old={"person": {"name": "Ann", "age": 40}, "is_valid": True},
            ctx={"roles": []},
        )

    def test_resolver_is_given_the_context(self):
        """A lookup can be scoped by the tenant, or whatever else the caller passes."""
        self._validate("post", {"person": {"name": "Ann"}}, ctx={"tenant": "acme", "roles": []})

        self.assertEqual(dict(self.contexts[0]), {"tenant": "acme", "roles": []})

    def test_the_context_the_resolver_gets_is_read_only(self):
        """A resolver cannot change what the rules go on to evaluate."""
        self._validate("post", {"person": {"name": "Ann"}}, ctx={"tenant": "acme"})

        with self.assertRaises(TypeError):
            self.contexts[0]["tenant"] = "other"

    def test_missing_required_lookup_is_a_failure_not_an_error(self):
        """A rule reading through a lookup that found nothing fails cleanly.

        Evaluating the expression would raise inside CEL and surface as a 500, so
        the rule is failed before it gets that far.
        """
        with self.assertRaises(self.genval.ValidationError) as ctx:
            self._validate("post", {"person": {"name": "Ann"}, "postal": "NOPE", "city": "Ottawa"})

        violation = ctx.exception.violations[0]
        self.assertEqual(violation.rule, "city_matches")
        self.assertEqual(violation.message, "No postal_codes found with name 'NOPE'.")
        self.assertEqual(violation.field, "postal")

    def test_optional_lookup_may_find_nothing(self):
        """A rule about absence passes when its lookup finds nothing."""
        self._validate("delete", old={"person": {"name": "Ann"}, "postal": "NOPE"})

    def test_optional_lookup_that_resolves(self):
        """The same rule fails when the thing it is checking for does exist."""
        with self.assertRaises(self.genval.ValidationError) as ctx:
            self._validate("delete", old={"person": {"name": "Ann"}, "postal": "K1A"})

        self.assertEqual(ctx.exception.violations[0].rule, "not_in_use")
        self.assertEqual(ctx.exception.status, 409)

    def test_subject_overrides_the_merge(self):
        """A caller can state the resulting resource instead of having it merged."""
        with self.assertRaises(self.genval.ValidationError) as ctx:
            asyncio.run(
                self.genval.validate(
                    "patch",
                    "addressbook",
                    body={"anything": "ignored"},
                    old={"person": {"name": "Ann"}, "is_valid": True},
                    subject={"person": {"name": "Bob"}, "is_valid": True},
                    resolver=self.resolver,
                    ctx={"roles": []},
                )
            )

        self.assertEqual(
            sorted(violation.rule for violation in ctx.exception.violations),
            ["person_is_immutable", "person_must_exist"],
        )

    def test_subject_is_used_verbatim(self):
        """Nothing from old leaks into a subject the caller worked out."""
        asyncio.run(
            self.genval.validate(
                "patch",
                "addressbook",
                body={},
                old={"person": {"name": "Ann"}, "is_valid": True},
                subject={"person": {"name": "Ann"}, "is_valid": True},
                resolver=self.resolver,
                ctx={"roles": []},
            )
        )

    def test_resolve_path(self):
        """Dotted paths report a missing field as missing, not as null."""
        runtime = importlib.import_module("genval.runtime")

        self.assertEqual(runtime.resolve_path({"a": {"b": 1}}, "a.b"), 1)
        self.assertIs(runtime.resolve_path({"a": {}}, "a.b"), self.genval.MISSING)
        self.assertIsNone(runtime.resolve_path({"a": {"b": None}}, "a.b"))


if __name__ == "__main__":
    unittest.main()
