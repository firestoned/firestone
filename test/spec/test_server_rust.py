# pylint: disable=duplicate-code
"""
Test the firestone.spec.server_rust module.
"""

import unittest

from firestone.spec import server_rust
from firestone.spec import validations


def _resource(kind: str = "addressbook", **extra) -> dict:
    """Get a minimal resource, with anything extra merged over it."""
    rsrc = {
        "kind": kind,
        "apiVersion": "v1",
        "metadata": {"description": f"An example {kind}"},
        "methods": {"resource": ["get", "post"], "instance": ["get", "put", "patch", "delete"]},
        "schema": {
            "type": "array",
            "key": {"name": f"{kind}_key", "schema": {"type": "string"}},
            "items": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "The city"},
                    "is_valid": {"type": "boolean"},
                    "people": {"type": "array", "items": {"type": "string"}},
                    "person": {"schema": {"items": {"type": "object", "properties": {}}}},
                },
                "required": ["city"],
            },
        },
    }
    rsrc.update(extra)

    return rsrc


def _generate(rsrc_data: list, **kwargs) -> dict:
    """Generate a server crate for the given resources."""
    return server_rust.generate(rsrc_data, "Title", "Description", "1.0", **kwargs)


class TestCrateVersion(unittest.TestCase):
    """Test firestone.spec.server_rust.crate_version()"""

    def test_padding(self):
        """An API version cargo would refuse is padded rather than rejected."""
        self.assertEqual(server_rust.crate_version("1.0"), "1.0.0")
        self.assertEqual(server_rust.crate_version("2"), "2.0.0")

    def test_already_semver(self):
        """A version cargo already accepts is left alone."""
        self.assertEqual(server_rust.crate_version("1.2.3"), "1.2.3")

    def test_not_a_number(self):
        """Something cargo could not parse at all falls back."""
        self.assertEqual(server_rust.crate_version("v-next"), "0.1.0")


class TestResources(unittest.TestCase):
    """Test firestone.spec.server_rust.resources()"""

    def test_defaults(self):
        """A resource is described in the shape the templates want."""
        described = server_rust.resources([_resource()])[0]

        self.assertEqual(described["module"], "addressbook")
        self.assertEqual(described["model"], "Addressbook")
        self.assertEqual(described["path"], "addressbook")
        self.assertEqual(described["key"], "addressbook_key")
        self.assertEqual(described["resource_methods"], ["get", "post"])
        self.assertEqual(described["instance_methods"], ["get", "put", "patch", "delete"])

    def test_plural_and_version_in_path(self):
        """The path follows the same rules the OpenAPI document does."""
        rsrc = _resource("proxy", plural="proxies", versionInPath=True)
        described = server_rust.resources([rsrc])[0]

        self.assertEqual(described["path"], "vv1/proxies")

    def test_only_declared_methods(self):
        """A method the schema does not declare is not routed."""
        rsrc = _resource(methods={"resource": ["get"], "instance": ["get"]})
        described = server_rust.resources([rsrc])[0]

        self.assertEqual(described["resource_methods"], ["get"])
        self.assertEqual(described["instance_methods"], ["get"])

    def test_property_types(self):
        """Properties map onto rust types, and what cannot be named stays JSON."""
        properties = {
            prop["field"]: prop for prop in server_rust.resources([_resource()])[0]["properties"]
        }

        self.assertEqual(properties["city"]["type"], "String")
        self.assertTrue(properties["city"]["required"])
        self.assertEqual(properties["is_valid"]["type"], "bool")
        self.assertFalse(properties["is_valid"]["required"])
        self.assertEqual(properties["people"]["type"], "Vec<String>")
        self.assertEqual(properties["person"]["type"], "serde_json::Value")

    def test_scalar_schema_keeps_its_type(self):
        """A property carrying its type under 'schema' is not treated as embedded."""
        rsrc = _resource()
        rsrc["schema"]["items"]["properties"]["code"] = {"schema": {"type": "integer"}}
        properties = {
            prop["field"]: prop for prop in server_rust.resources([rsrc])[0]["properties"]
        }

        self.assertEqual(properties["code"]["type"], "i64")

    def test_security_is_carried_through(self):
        """The schema decides which operations the router puts behind a token."""
        rsrc = _resource(
            security={"scheme": {"bearer_auth": {"type": "http"}}, "resource": ["post"]}
        )
        described = server_rust.resources([rsrc])[0]

        self.assertEqual(described["secured_resource"], ["post"])
        self.assertEqual(described["secured_instance"], [])

    def test_security_without_a_scheme_secures_nothing(self):
        """A security block with no scheme cannot gate anything."""
        described = server_rust.resources([_resource(security={"resource": ["post"]})])[0]

        self.assertEqual(described["secured_resource"], [])

    def test_query_params_are_deduplicated(self):
        """A parameter declared twice is only accepted once."""
        rsrc = _resource(default_query_params=[{"name": "limit", "schema": {"type": "integer"}}])
        rsrc["schema"]["query_params"] = [
            {"name": "limit", "schema": {"type": "integer"}},
            {"name": "city", "schema": {"type": "string"}},
        ]
        params = server_rust.resources([rsrc])[0]["query_params"]

        self.assertEqual([param["name"] for param in params], ["limit", "city"])


class TestAttributes(unittest.TestCase):
    """Test how firestone.spec.server_rust routes a resource's attributes."""

    def test_attrs_follow_expose(self):
        """A property the schema hides has no endpoint, as in the OpenAPI document."""
        rsrc = _resource(methods={"resource": ["get"], "instance_attrs": ["get", "put"]})
        rsrc["schema"]["items"]["properties"]["secret"] = {"type": "string", "expose": False}
        described = server_rust.resources([rsrc])[0]

        self.assertIn("city", described["attrs"])
        self.assertNotIn("secret", described["attrs"])

    def test_attr_methods(self):
        """Only the methods instance_attrs declares are routed."""
        rsrc = _resource(methods={"resource": ["get"], "instance_attrs": ["get", "delete"]})
        described = server_rust.resources([rsrc])[0]

        self.assertEqual(described["attr_methods"], ["get", "delete"])

    def test_no_attr_routes_without_instance_attrs(self):
        """A resource that declares none gets no attribute route."""
        routes = _generate([_resource()])["src/routes.rs"]

        self.assertNotIn("{attr}", routes)

    def test_attr_route_is_parameterised(self):
        """One route per resource, not one per property."""
        rsrc = _resource(methods={"resource": ["get"], "instance_attrs": ["get", "put"]})
        files = _generate([rsrc])

        self.assertIn('"/addressbook/{addressbook_key}/{attr}"', files["src/routes.rs"])
        self.assertIn("get(handlers::addressbook::get_attr)", files["src/routes.rs"])
        self.assertIn("const ATTRS: &[&str] = &[", files["src/handlers.rs"])

    def test_attr_put_validates_the_whole_resource(self):
        """The rules are written against the resource, so they get it, not the field."""
        rsrc = _resource(
            methods={"resource": ["get"], "instance_attrs": ["put"]},
            validations={"rules": [{"name": "r", "expr": "true"}]},
        )
        ruleset = validations.extract([rsrc])
        handlers = _generate(validations.strip([rsrc]), ruleset=ruleset)["src/handlers.rs"]

        self.assertIn('validate_subject(&state, "put", RESOURCE, &updated', handlers)

    def test_secured_attrs_are_wrapped(self):
        """instance_attrs security gates the attribute routes."""
        rsrc = _resource(
            methods={"resource": ["get"], "instance_attrs": ["get", "put"]},
            security={
                "scheme": {"bearer_auth": {"type": "http"}},
                "instance_attrs": ["put"],
            },
        )
        routes = _generate([rsrc])["src/routes.rs"]
        secured = routes.split("let secured")[1]

        self.assertIn("put(handlers::addressbook::put_attr)", secured)
        self.assertIn("require_bearer", secured)


class TestGenerate(unittest.TestCase):
    """Test firestone.spec.server_rust.generate()"""

    def test_files(self):
        """A crate that cargo can build is generated."""
        files = _generate([_resource()])

        for name in (
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
        ):
            self.assertIn(name, files)

    def test_no_validation_module_without_rules(self):
        """A project with no rules gets no validation module and no CEL dependency."""
        files = _generate([_resource()])

        self.assertNotIn("src/validation/mod.rs", files)
        self.assertNotIn("src/resolver.rs", files)
        self.assertNotIn("cel-interpreter", files["Cargo.toml"])
        self.assertNotIn("pub mod validation;", files["src/lib.rs"])

    def test_validation_is_wired_in(self):
        """A project with rules gets the package, the resolver and the handler calls."""
        rsrc = _resource(validations={"rules": [{"name": "r", "expr": "true"}]})
        ruleset = validations.extract([rsrc])
        files = _generate(validations.strip([rsrc]), ruleset=ruleset)

        self.assertIn("src/validation/mod.rs", files)
        self.assertIn("src/resolver.rs", files)
        self.assertIn("cel-interpreter", files["Cargo.toml"])
        self.assertIn('validate_request(&state, "post"', files["src/handlers.rs"])

    def test_validation_can_be_turned_off(self):
        """The rules can be left out even when the resources declare them."""
        rsrc = _resource(validations={"rules": [{"name": "r", "expr": "true"}]})
        ruleset = validations.extract([rsrc])
        files = _generate(validations.strip([rsrc]), ruleset=ruleset, with_validations=False)

        self.assertNotIn("src/validation/mod.rs", files)
        self.assertNotIn("validate_request", files["src/handlers.rs"])

    def test_routes_follow_the_declared_methods(self):
        """A method the schema does not declare gets no route."""
        rsrc = _resource(methods={"resource": ["get"], "instance": ["get"]})
        routes = _generate([rsrc])["src/routes.rs"]

        self.assertIn("get(handlers::addressbook::get_collection)", routes)
        self.assertNotIn("post(handlers::addressbook::post_collection)", routes)

    def test_only_secured_routes_are_wrapped(self):
        """The bearer check covers what the schema said, and nothing else."""
        rsrc = _resource(
            security={"scheme": {"bearer_auth": {"type": "http"}}, "resource": ["post"]}
        )
        routes = _generate([rsrc])["src/routes.rs"]
        secured = routes.split("let secured")[1]
        open_routes = routes.split("let secured")[0]

        self.assertIn("post(handlers::addressbook::post_collection)", secured)
        self.assertIn("require_bearer", secured)
        self.assertIn("get(handlers::addressbook::get_collection)", open_routes)

    def test_no_secured_router_without_security(self):
        """A project with nothing secured does not build an empty secured router."""
        routes = _generate([_resource()])["src/routes.rs"]

        self.assertNotIn("let secured", routes)
        self.assertNotIn("require_bearer", routes)

    def test_only_the_verbs_used_are_imported(self):
        """An unused import would be a warning in the consumer's build."""
        rsrc = _resource(methods={"resource": ["get"], "instance": ["get"]})
        routes = _generate([rsrc])["src/routes.rs"]

        self.assertIn("use axum::routing::get;", routes)
        self.assertNotIn("use axum::routing::patch;", routes)

    def test_crate_version_is_semver(self):
        """The API version is padded so cargo will take it."""
        self.assertIn('version = "1.0.0"', _generate([_resource()])["Cargo.toml"])

    def test_generation_is_idempotent(self):
        """Regenerating without changing a schema changes nothing."""
        self.assertEqual(_generate([_resource()]), _generate([_resource()]))


if __name__ == "__main__":
    unittest.main()
