# pylint: disable=duplicate-code
"""
Test the firestone.spec.server_rust module.
"""

import unittest

import yaml

from firestone.spec import openapi
from firestone.spec import server_rust
from firestone.spec import validations


def _resource(kind: str = "addressbook", **extra) -> dict:
    """Get a minimal resource, with anything extra merged over it."""
    rsrc = {
        "kind": kind,
        "apiVersion": "v1",
        "metadata": {"description": f"An example {kind}"},
        "methods": {"resource": ["get", "post"], "instance": ["get", "put", "delete"]},
        "schema": {
            "type": "array",
            "key": {"name": f"{kind}_key", "schema": {"type": "string"}},
            "items": {
                "type": "object",
                "properties": {"city": {"type": "string"}, "is_valid": {"type": "boolean"}},
                "required": ["city"],
            },
        },
    }
    rsrc.update(extra)

    return rsrc


def _spec(rsrc_data: list) -> dict:
    """Get the OpenAPI document the server would be generated from."""
    return yaml.safe_load(openapi.generate(rsrc_data, "Title", "Desc", "Sum", "1.0"))


def _generate(rsrc_data: list, **kwargs) -> dict:
    """Generate an implementation crate for the given resources."""
    return server_rust.generate(rsrc_data, "Title", "Desc", "1.0", **kwargs)


class TestNaming(unittest.TestCase):
    """Test that firestone derives the names openapi-generator generates."""

    def test_pascal_keeps_inner_capitals(self):
        """CreatePostal_code is the component name, CreatePostalCode is the struct."""
        self.assertEqual(server_rust.pascal("create_postal_code"), "CreatePostalCode")
        self.assertEqual(server_rust.pascal("CreatePostal_code"), "CreatePostalCode")
        self.assertEqual(server_rust.pascal("persons_uuid_get"), "PersonsUuidGet")

    def test_variant_from_a_description(self):
        """A response variant is Status<code>_<description>, capitals preserved."""
        self.assertEqual(server_rust.variant(200, "Response for OK"), "Status200_ResponseForOK")
        self.assertEqual(
            server_rust.variant(422, "One or more validation rules failed"),
            "Status422_OneOrMoreValidationRulesFailed",
        )

    def test_default_is_status_zero(self):
        """openapi-generator numbers a 'default' response 0."""
        self.assertEqual(
            server_rust.variant("default", "Default HEAD response"), "Status0_DefaultHEADResponse"
        )

    def test_crate_version_is_padded(self):
        """An API version cargo would refuse is padded rather than rejected."""
        self.assertEqual(server_rust.crate_version("1.0"), "1.0.0")
        self.assertEqual(server_rust.crate_version("1.2.3"), "1.2.3")
        self.assertEqual(server_rust.crate_version("v-next"), "0.1.0")


class TestOperations(unittest.TestCase):
    """Test firestone.spec.server_rust.operations()"""

    def test_every_operation_is_described(self):
        """Nothing the document declares is left without an implementation."""
        spec = _spec([_resource()])
        declared = sum(
            1
            for path in spec["paths"]
            for method in spec["paths"][path]
            if isinstance(spec["paths"][path][method], dict)
        )
        described = sum(
            len(trait["operations"]) for trait in server_rust.operations(spec, {}).values()
        )

        self.assertEqual(described, declared)

    def test_grouped_by_tag(self):
        """Operations are grouped the way openapi-generator groups its traits."""
        traits = server_rust.operations(_spec([_resource()]), {})

        self.assertEqual(list(traits), ["addressbook"])
        self.assertEqual(traits["addressbook"]["trait"], "Addressbook")

    def test_shapes(self):
        """A path is a collection, an instance or one attribute of an instance."""
        traits = server_rust.operations(_spec([_resource()]), {})
        shapes = {op["name"]: op["shape"] for op in traits["addressbook"]["operations"]}

        self.assertEqual(shapes["addressbook_get"], "collection")
        self.assertEqual(shapes["addressbook_addressbook_key_get"], "instance")

    def test_claims_follow_security(self):
        """Only an operation the schema secured carries claims."""
        rsrc = _resource(
            security={"scheme": {"bearer_auth": {"type": "http"}}, "resource": ["post"]}
        )
        traits = server_rust.operations(_spec([rsrc]), {})
        claims = {op["name"]: op["claims"] for op in traits["addressbook"]["operations"]}

        self.assertTrue(claims["addressbook_post"])
        self.assertFalse(claims["addressbook_get"])

    def test_trait_declares_claims_only_when_needed(self):
        """A trait with no secured operation has no associated Claims type."""
        plain = server_rust.operations(_spec([_resource()]), {})
        secured = server_rust.operations(
            _spec(
                [
                    _resource(
                        security={
                            "scheme": {"bearer_auth": {"type": "http"}},
                            "resource": ["post"],
                        }
                    )
                ]
            ),
            {},
        )

        self.assertFalse(plain["addressbook"]["claims"])
        self.assertTrue(secured["addressbook"]["claims"])

    def test_body_types(self):
        """A body is the model openapi-generator names, or a plain rust type."""
        traits = server_rust.operations(_spec([_resource()]), {})
        bodies = {op["name"]: op["body"] for op in traits["addressbook"]["operations"]}

        self.assertEqual(bodies["addressbook_post"], "models::CreateAddressbook")
        self.assertIsNone(bodies["addressbook_get"])


class TestActions(unittest.TestCase):
    """Test that firestone only claims the operations it writes a body for."""

    def test_action_table(self):
        """One place decides what a handler does, so the template cannot drift."""
        cases = [
            (("collection", "get", None, True), "list"),
            (("collection", "post", "models::X", True), "create"),
            (("collection", "post", None, True), None),
            (("collection", "delete", None, True), None),
            (("collection", "patch", None, True), None),
            (("instance", "get", None, True), "fetch"),
            (("instance", "put", "models::X", True), "update"),
            (("instance", "patch", "models::X", True), "update"),
            (("instance", "patch", None, True), None),
            (("instance", "delete", None, True), "remove"),
            (("attribute", "get", None, True), "attr_get"),
            (("attribute", "put", "String", True), "attr_set"),
            (("attribute", "post", "String", True), None),
            (("attribute", "patch", "String", True), None),
            (("attribute", "delete", None, True), "attr_remove"),
            (("instance", "head", None, True), "head"),
            (("instance", "get", None, None), None),
        ]
        for (shape, method, body, success), expected in cases:
            # pylint: disable=protected-access
            actual = server_rust._action(
                shape, method, body, {"payload": True} if success else None
            )
            self.assertEqual(actual, expected, f"{shape} {method} body={body}")

    def test_attribute_post_and_patch_are_not_a_replace(self):
        """A POST appends and a PATCH merges; neither is silently a PUT."""
        # pylint: disable=protected-access
        success = {"payload": True}
        self.assertEqual(server_rust._action("attribute", "put", "String", success), "attr_set")
        self.assertIsNone(server_rust._action("attribute", "post", "String", success))
        self.assertIsNone(server_rust._action("attribute", "patch", "String", success))

    def test_unimplemented_operations_answer_501(self):
        """An operation firestone does not write a body for says so."""
        rsrc = _resource(methods={"resource": ["get", "delete"]})
        handlers = _generate([rsrc])["src/handlers.rs"]

        self.assertIn("Error::NotImplemented(", handlers)
        self.assertIn("is not generated; implement it by hand", handlers)

    def test_arguments_nothing_reads_are_bound_to_underscore(self):
        """An unused argument is a warning, and the gate treats warnings as errors."""
        rsrc = _resource(methods={"instance": ["head"]})
        handlers = _generate([rsrc])["src/handlers.rs"]

        self.assertIn("_path_params: &models::", handlers)
        self.assertNotIn("\n        path_params: &models::", handlers)


class TestImports(unittest.TestCase):
    """Test that handlers.rs imports only what its operations reach for."""

    @staticmethod
    def _imports(rsrc: dict) -> list:
        return [
            line
            for line in _generate([rsrc])["src/handlers.rs"].split("\n")
            if line.startswith("use ")
        ]

    def test_post_only_needs_no_value(self):
        """serde_json::Value is only reached for by a collection list."""
        imports = self._imports(_resource(methods={"resource": ["post"]}))

        self.assertNotIn("use serde_json::Value;", imports)

    def test_get_only_needs_no_models_or_to_json(self):
        """Neither is reached for when nothing carries a body."""
        imports = self._imports(_resource(methods={"resource": ["get"]}))

        self.assertNotIn("use openapi::models;", imports)
        self.assertNotIn("use crate::error::to_json;", imports)

    def test_a_full_resource_needs_all_of_them(self):
        """And they are imported where they are used."""
        imports = self._imports(
            _resource(methods={"resource": ["get", "post"], "instance": ["get", "put"]})
        )

        self.assertIn("use serde_json::Value;", imports)
        self.assertIn("use openapi::models;", imports)
        self.assertIn("use crate::error::to_json;", imports)
        self.assertIn("use crate::error::from_json;", imports)

    def test_auth_is_only_generated_when_something_is_secured(self):
        """The generated server only declares ApiAuthBasic when the schema secures
        something, so implementing it unconditionally does not compile."""
        plain = _generate([_resource()])
        secured = _generate(
            [
                _resource(
                    security={"scheme": {"bearer_auth": {"type": "http"}}, "resource": ["post"]}
                )
            ]
        )

        self.assertNotIn("src/auth.rs", plain)
        self.assertNotIn("pub mod auth;", plain["src/lib.rs"])
        self.assertIn("src/auth.rs", secured)
        self.assertIn("pub mod auth;", secured["src/lib.rs"])
        self.assertIn("subtle", secured["Cargo.toml"])


class TestTypes(unittest.TestCase):
    """Test that firestone names the same rust types openapi-generator does."""

    def test_format_decides_the_integer_width(self):
        """An int64 sent as i32 would not satisfy the trait the server declares."""
        self.assertEqual(server_rust.rust_type({"type": "integer"}), "i32")
        self.assertEqual(server_rust.rust_type({"type": "integer", "format": "int64"}), "i64")
        self.assertEqual(server_rust.rust_type({"type": "number", "format": "float"}), "f32")

    def test_an_unmapped_type_has_no_rust_name(self):
        """Falling back is the caller's decision, not this function's."""
        self.assertIsNone(server_rust.rust_type({"type": "who-knows"}))


class TestMetadata(unittest.TestCase):
    """Test that a title or description cannot break what it is written into."""

    @staticmethod
    def _generate(title: str, desc: str) -> dict:
        return server_rust.generate([_resource()], title, desc, "1.0")

    def test_a_quote_does_not_break_the_manifest(self):
        """Cargo.toml is TOML, so the description is a TOML string."""
        files = self._generate("T", 'Line "one" two')

        self.assertIn('description = "Line \\"one\\" two"', files["Cargo.toml"])

    def test_a_brace_does_not_break_the_format_string(self):
        """The title goes inside a rust format string, where a brace is an argument."""
        files = self._generate("A {brace} title", "D")

        self.assertIn("A {{brace}} title", files["src/main.rs"])

    def test_a_quote_does_not_break_the_format_string(self):
        """And a quote would end the literal."""
        files = self._generate('A "quoted" title', "D")

        self.assertIn('A \\"quoted\\" title', files["src/main.rs"])

    def test_a_newline_does_not_break_a_doc_comment(self):
        """A doc comment ends at the newline, so the text is flattened."""
        files = self._generate("T", "Line one\nline two")

        self.assertIn("//! Line one line two", files["src/lib.rs"])


class TestOwnership(unittest.TestCase):
    """Test which files firestone owns and which are yours once they exist."""

    def test_only_what_follows_the_document_is_regenerated(self):
        """Everything else is scaffolded once, so your Backend survives."""
        self.assertEqual(
            sorted(server_rust.GENERATED),
            ["src/handlers.rs", "src/lib.rs", "tests/api.rs"],
        )
        for name in ("src/backend.rs", "src/auth.rs", "src/main.rs", "Cargo.toml"):
            self.assertIn(name, server_rust.SCAFFOLD)

        # lib.rs declares the modules, which depend on whether the schema secures
        # anything: keeping it would leave a crate that does not compile.
        self.assertNotIn("src/lib.rs", server_rust.SCAFFOLD)

    def test_every_template_is_one_or_the_other(self):
        """A file that is neither would be written with no rule about it."""
        self.assertEqual(
            sorted(server_rust.TEMPLATES),
            sorted(server_rust.GENERATED + server_rust.SCAFFOLD),
        )


class TestGeneratedTests(unittest.TestCase):
    """Test the test suite firestone generates alongside the implementation."""

    def test_a_create_is_checked_for_its_key(self):
        """The response of a create has to carry the key it was given."""
        rsrc = _resource()
        rsrc["schema"]["items"]["properties"]["addressbook_key"] = {"type": "string"}
        tests = _generate([rsrc])["tests/api.rs"]

        self.assertIn("addressbook_create_returns_a_usable_key", tests)
        self.assertIn('.get("addressbook_key")', tests)

    def test_no_key_test_when_the_model_does_not_declare_one(self):
        """serde drops a field the struct does not have, so the key cannot come back.

        Claiming it would generate a test that panics on every such schema.
        """
        tests = _generate([_resource()])["tests/api.rs"]

        self.assertNotIn("create_returns_a_usable_key", tests)

    def test_no_seed_of_another_schemas_resources(self):
        """A seed for the addressbook's persons is meaningless in another project."""
        rsrc = _resource()
        rsrc["schema"]["items"]["properties"]["addressbook_key"] = {"type": "string"}
        tests = _generate([rsrc])["tests/api.rs"]

        self.assertNotIn('seed("persons"', tests)

    def test_paths_are_filled_in(self):
        """A test asks for a concrete path, not one with a parameter in it."""
        tests = _generate([_resource()])["tests/api.rs"]

        self.assertNotIn("{addressbook_key}", tests)
        self.assertIn("/addressbook/test-key", tests)

    def test_the_sample_body_satisfies_the_model(self):
        """A create test has to post something the request validation accepts."""
        rsrc = _resource()
        rsrc["schema"]["items"]["properties"]["kind_of"] = {
            "type": "string",
            "enum": ["one", "two"],
        }
        rsrc["schema"]["items"]["required"] = ["city", "kind_of"]
        rsrc["schema"]["items"]["properties"]["addressbook_key"] = {"type": "string"}
        tests = _generate([rsrc])["tests/api.rs"]

        self.assertIn('\\"city\\": \\"x\\"', tests)
        self.assertIn('\\"kind_of\\": \\"one\\"', tests)

    def test_auth_tests_only_when_something_is_secured(self):
        """There is nothing to check when the schema secures nothing."""
        plain = _generate([_resource()])["tests/api.rs"]
        secured = _generate(
            [
                _resource(
                    security={"scheme": {"bearer_auth": {"type": "http"}}, "resource": ["post"]}
                )
            ]
        )["tests/api.rs"]

        self.assertNotIn("a_secured_operation_needs_a_token", plain)
        self.assertIn("a_secured_operation_needs_a_token", secured)
        self.assertIn("a_lowercase_scheme_is_accepted", secured)


class TestGenerate(unittest.TestCase):
    """Test firestone.spec.server_rust.generate()"""

    def test_files(self):
        """The crate that implements the generated server's traits."""
        files = _generate([_resource()])

        for name in (
            "Cargo.toml",
            "src/main.rs",
            "src/lib.rs",
            "src/error.rs",
            "src/backend.rs",
            "src/handlers.rs",
        ):
            self.assertIn(name, files)

        # auth.rs only when the schema secures something; see TestImports.
        self.assertNotIn("src/auth.rs", files)

    def test_it_depends_on_the_generated_server(self):
        """The implementation is a sibling crate of the openapi-generator output."""
        files = _generate([_resource()], api_pkg="addressbook_api")

        self.assertIn('addressbook_api = { path = "../api" }', files["Cargo.toml"])
        self.assertIn("use addressbook_api::apis;", files["src/handlers.rs"])

    def test_every_operation_is_implemented(self):
        """One method per operation, or the server does not compile."""
        spec = _spec([_resource()])
        files = _generate([_resource()])
        for path in spec["paths"]:
            for method in spec["paths"][path]:
                operation = spec["paths"][path][method]
                if isinstance(operation, dict) and "operationId" in operation:
                    self.assertIn(f"async fn {operation['operationId']}(", files["src/handlers.rs"])

    def test_no_validation_module_without_rules(self):
        """A project with no rules gets no validation module and no CEL dependency."""
        files = _generate([_resource()])

        self.assertNotIn("src/validation/mod.rs", files)
        self.assertNotIn("src/resolver.rs", files)
        self.assertNotIn("cel-interpreter", files["Cargo.toml"])

    def test_validation_is_wired_in(self):
        """A project with rules gets the package, the resolver and the handler calls."""
        rsrc = _resource(validations={"rules": [{"name": "r", "expr": "true"}]})
        ruleset = validations.extract([rsrc])
        files = _generate(validations.strip([rsrc]), ruleset=ruleset)

        self.assertIn("src/validation/mod.rs", files)
        self.assertIn("src/resolver.rs", files)
        self.assertIn("validate_request(self,", files["src/handlers.rs"])

    def test_validation_can_be_turned_off(self):
        """The rules can be left out even when the resources declare them."""
        rsrc = _resource(validations={"rules": [{"name": "r", "expr": "true"}]})
        ruleset = validations.extract([rsrc])
        files = _generate(validations.strip([rsrc]), ruleset=ruleset, with_validations=False)

        self.assertNotIn("src/validation/mod.rs", files)
        self.assertNotIn("validate_request", files["src/handlers.rs"])

    def test_generation_is_idempotent(self):
        """Regenerating without changing a schema changes nothing."""
        self.assertEqual(_generate([_resource()]), _generate([_resource()]))


if __name__ == "__main__":
    unittest.main()
