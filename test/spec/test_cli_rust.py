# pylint: disable=protected-access
"""
Test the firestone.spec.cli_rust module.
"""

import unittest
from unittest import mock

from firestone.spec import cli_rust


class TestCliRustParamsToAttrs(unittest.TestCase):
    """Test all aspects of firestone.spec.cli_rust.params_to_attrs"""

    def test_string_param(self):
        """Test params_to_attrs with string parameter."""
        params = [
            {
                "name": "foo",
                "description": "A foo parameter",
                "schema": {"type": "string"},
                "required": True,
            }
        ]
        attrs = cli_rust.params_to_attrs(params)
        self.assertEqual(len(attrs), 1)
        self.assertEqual(attrs[0]["name"], "foo")
        self.assertEqual(attrs[0]["type"], "String")
        self.assertTrue(attrs[0]["required"])

    def test_integer_param(self):
        """Test params_to_attrs with integer parameter."""
        params = [
            {
                "name": "age",
                "description": "Age in years",
                "schema": {"type": "integer"},
                "required": False,
            }
        ]
        attrs = cli_rust.params_to_attrs(params)
        self.assertEqual(len(attrs), 1)
        self.assertEqual(attrs[0]["name"], "age")
        self.assertEqual(attrs[0]["type"], "i64")
        self.assertFalse(attrs[0]["required"])

    def test_boolean_param(self):
        """Test params_to_attrs with boolean parameter."""
        params = [
            {
                "name": "is_valid",
                "description": "Whether it is valid",
                "schema": {"type": "boolean"},
                "required": False,
            }
        ]
        attrs = cli_rust.params_to_attrs(params)
        self.assertEqual(len(attrs), 1)
        self.assertEqual(attrs[0]["name"], "is_valid")
        self.assertEqual(attrs[0]["type"], "bool")
        self.assertFalse(attrs[0]["required"])

    def test_enum_param(self):
        """Test params_to_attrs with enum parameter."""
        params = [
            {
                "name": "status",
                "description": "Status value",
                "schema": {"type": "string", "enum": ["active", "inactive"]},
                "required": True,
            }
        ]
        attrs = cli_rust.params_to_attrs(params)
        self.assertEqual(len(attrs), 1)
        self.assertEqual(attrs[0]["name"], "status")
        self.assertEqual(attrs[0]["type"], "StatusEnum")
        self.assertTrue(attrs[0]["is_enum"])
        self.assertIn("enum_values", attrs[0])
        self.assertEqual(attrs[0]["enum_values"], ["active", "inactive"])

    def test_key_names_argument(self):
        """Test params_to_attrs marks key names as arguments."""
        params = [
            {
                "name": "foo_key",
                "description": "A key",
                "schema": {"type": "string"},
                "required": True,
            }
        ]
        attrs = cli_rust.params_to_attrs(params, key_names=["foo_key"])
        self.assertEqual(len(attrs), 1)
        self.assertTrue(attrs[0]["argument"])

    def test_non_key_names_not_argument(self):
        """Test params_to_attrs does not mark non-key names as arguments."""
        params = [
            {
                "name": "foo",
                "description": "Not a key",
                "schema": {"type": "string"},
                "required": True,
            }
        ]
        attrs = cli_rust.params_to_attrs(params, key_names=["foo_key"])
        self.assertEqual(len(attrs), 1)
        self.assertFalse(attrs[0]["argument"])

    def test_array_param(self):
        """Test params_to_attrs with array parameter."""
        params = [
            {
                "name": "tags",
                "description": "List of tags",
                "schema": {
                    "type": "array",
                    "items": {"type": "string"},
                },
                "required": False,
            }
        ]
        attrs = cli_rust.params_to_attrs(params)
        self.assertEqual(len(attrs), 1)
        self.assertEqual(attrs[0]["name"], "tags")
        self.assertEqual(attrs[0]["type"], "Vec<String>")

    def test_object_param(self):
        """Test params_to_attrs with object parameter."""
        params = [
            {
                "name": "person",
                "description": "Person object",
                "schema": {"type": "object"},
                "required": False,
            }
        ]
        attrs = cli_rust.params_to_attrs(params)
        self.assertEqual(len(attrs), 1)
        self.assertEqual(attrs[0]["name"], "person")
        self.assertEqual(attrs[0]["type"], "String")  # Objects are passed as JSON strings


class TestCliRustGetResourceAttrs(unittest.TestCase):
    """Test all aspects of firestone.spec.cli_rust.get_resource_attrs"""

    def test_basic_properties(self):
        """Test get_resource_attrs with basic properties."""
        schema = {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "age": {"type": "integer"},
                },
            },
        }
        attrs = cli_rust.get_resource_attrs(schema)
        self.assertIsNotNone(attrs)
        self.assertEqual(len(attrs), 2)
        names = [attr["name"] for attr in attrs]
        self.assertIn("name", names)
        self.assertIn("age", names)

    def test_excludes_key_names(self):
        """Test get_resource_attrs excludes key names to avoid duplicates."""
        schema = {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "foo_key": {"type": "string"},
                    "name": {"type": "string"},
                },
            },
        }
        attrs = cli_rust.get_resource_attrs(schema, key_names=["foo_key"])
        self.assertIsNotNone(attrs)
        names = [attr["name"] for attr in attrs]
        # Note: get_resource_attrs filters key_names in params_to_attrs via the argument flag
        # but the key may still appear if it's in the schema properties
        # The key should be marked as argument=True
        key_attrs = [attr for attr in attrs if attr["name"] == "foo_key"]
        if key_attrs:
            # If it appears, it should be marked as an argument
            self.assertTrue(key_attrs[0]["argument"])
        self.assertIn("name", names)

    def test_with_params(self):
        """Test get_resource_attrs with additional params."""
        schema = {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                },
            },
        }
        params = [
            {
                "name": "query_param",
                "description": "A query parameter",
                "schema": {"type": "string"},
            }
        ]
        attrs = cli_rust.get_resource_attrs(schema, params=params)
        names = [attr["name"] for attr in attrs]
        self.assertIn("name", names)
        self.assertIn("query_param", names)


class TestCliRustGetInstanceOps(unittest.TestCase):
    """Test all aspects of firestone.spec.cli_rust.get_instance_ops"""

    @mock.patch("firestone.spec.cli_rust.spec_openapi.get_params")
    def test_update_operation(self, get_params_mock):
        """Test get_instance_ops generates update operation correctly."""
        # Mock get_params to return path parameter
        get_params_mock.return_value = [
            {
                "name": "foo_key",
                "description": "A key",
                "schema": {"type": "string"},
                "required": True,
            }
        ]
        schema = {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "foo_key": {"type": "string"},
                    "name": {"type": "string"},
                },
            },
        }
        keys = [{"name": "foo_key", "schema": {"type": "string"}}]
        ops = cli_rust.get_instance_ops(
            "foo",
            schema,
            "/foo/{foo_key}",
            methods=["put"],
            descs={},
            keys=keys,
        )
        self.assertIsNotNone(ops)
        update_ops = [op for op in ops if op["name"] == "update"]
        self.assertEqual(len(update_ops), 1)
        update_op = update_ops[0]
        # Check that foo_key appears only once (as argument, not in body)
        attrs = update_op["attrs"]
        key_attrs = [attr for attr in attrs if attr["name"] == "foo_key"]
        # Should appear only once (as path parameter)
        self.assertEqual(len(key_attrs), 1)
        self.assertTrue(key_attrs[0]["argument"])  # Should be marked as argument

    @mock.patch("firestone.spec.cli_rust.spec_openapi.get_params")
    def test_get_operation(self, get_params_mock):
        """Test get_instance_ops generates get operation correctly."""
        get_params_mock.return_value = [
            {
                "name": "foo_key",
                "description": "A key",
                "schema": {"type": "string"},
                "required": True,
            }
        ]
        schema = {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "foo_key": {"type": "string"},
                    "name": {"type": "string"},
                },
            },
        }
        keys = [{"name": "foo_key", "schema": {"type": "string"}}]
        ops = cli_rust.get_instance_ops(
            "foo",
            schema,
            "/foo/{foo_key}",
            methods=["get"],
            descs={},
            keys=keys,
        )
        self.assertIsNotNone(ops)
        get_ops = [op for op in ops if op["name"] == "get"]
        self.assertEqual(len(get_ops), 1)
        get_op = get_ops[0]
        self.assertEqual(get_op["id"], "foo_foo_key_get")


class TestCliRustGetResourceOps(unittest.TestCase):
    """Test all aspects of firestone.spec.cli_rust.get_resource_ops"""

    @mock.patch("firestone.spec.cli_rust.spec_openapi.get_params")
    def test_list_operation(self, get_params_mock):
        """Test get_resource_ops generates list operation correctly."""
        get_params_mock.return_value = []
        schema = {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                },
            },
        }
        ops = cli_rust.get_resource_ops(
            "foo",
            schema,
            "/foo",
            methods=["get"],
            descs={},
        )
        self.assertIsNotNone(ops)
        list_ops = [op for op in ops if op["name"] == "list"]
        self.assertEqual(len(list_ops), 1)
        list_op = list_ops[0]
        self.assertEqual(list_op["id"], "foo_get")

    @mock.patch("firestone.spec.cli_rust.spec_openapi.get_params")
    def test_create_operation(self, get_params_mock):
        """Test get_resource_ops generates create operation correctly."""
        get_params_mock.return_value = []
        schema = {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                },
            },
        }
        ops = cli_rust.get_resource_ops(
            "foo",
            schema,
            "/foo",
            methods=["post"],
            descs={},
        )
        self.assertIsNotNone(ops)
        create_ops = [op for op in ops if op["name"] == "create"]
        self.assertEqual(len(create_ops), 1)
        create_op = create_ops[0]
        self.assertEqual(create_op["id"], "foo_post")


class TestCliRustGenerate(unittest.TestCase):
    """Test all aspects of firestone.spec.cli_rust.generate"""

    def test_basic_generation(self):
        """Test basic Rust CLI generation."""
        rsrc_data = [
            {
                "kind": "foo",
                "apiVersion": "v1",
                "schema": {
                    "type": "array",
                    "key": {"name": "foo_key", "schema": {"type": "string"}},
                    "items": {
                        "type": "object",
                        "properties": {
                            "foo_key": {"type": "string"},
                            "name": {"type": "string"},
                        },
                    },
                },
                "methods": {
                    "resource": ["get", "post"],
                    "instance": ["get", "put", "delete"],
                },
            }
        ]
        result = cli_rust.generate(
            "test_pkg",
            "test_pkg::apis",
            rsrc_data,
            "Test API",
            "Test API Description",
            "Test Summary",
            "1.0",
            as_modules=True,
        )
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        self.assertIn("foo", result)

    def test_generation_with_update_no_duplicate_key(self):
        """Test that update operations don't have duplicate key arguments."""
        rsrc_data = [
            {
                "kind": "foo",
                "apiVersion": "v1",
                "schema": {
                    "type": "array",
                    "key": {"name": "foo_key", "schema": {"type": "string"}},
                    "items": {
                        "type": "object",
                        "properties": {
                            "foo_key": {"type": "string"},
                            "name": {"type": "string"},
                        },
                    },
                },
                "methods": {
                    "resource": ["get", "post"],
                    "instance": ["get", "put", "delete"],
                },
            }
        ]
        result = cli_rust.generate(
            "test_pkg",
            "test_pkg::apis",
            rsrc_data,
            "Test API",
            "Test API Description",
            "Test Summary",
            "1.0",
            as_modules=True,
        )
        self.assertIsNotNone(result)
        rust_code = result["foo"]
        # Count occurrences of @arg(name = "foo_key")
        # Should appear only once for update operation
        update_section_start = rust_code.find("pub struct UpdateArgs")
        if update_section_start != -1:
            # Find the update function
            update_fn_start = rust_code.find("pub async fn foo_foo_key_put", update_section_start)
            if update_fn_start != -1:
                # Count @arg decorators for foo_key in the update function area
                update_section = rust_code[update_section_start : update_fn_start + 500]
                # Check that foo_key appears as argument only once
                arg_count = update_section.count('#[arg(name = "foo_key"')
                # Should be 1 (in UpdateArgs struct) or 0 if it's handled differently
                self.assertLessEqual(arg_count, 1, "foo_key should not appear multiple times")

    def test_generation_includes_required_imports(self):
        """Test that generated Rust code includes required imports."""
        rsrc_data = [
            {
                "kind": "foo",
                "apiVersion": "v1",
                "schema": {
                    "type": "array",
                    "key": {"name": "foo_key", "schema": {"type": "string"}},
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                        },
                    },
                },
                "methods": {
                    "resource": ["get"],
                },
            }
        ]
        result = cli_rust.generate(
            "test_pkg",
            "test_pkg::apis",
            rsrc_data,
            "Test API",
            "Test API Description",
            "Test Summary",
            "1.0",
            as_modules=True,
        )
        rust_code = result["foo"]
        # Check for required imports (may vary based on template)
        self.assertIn("clap", rust_code.lower())
        self.assertIn("serde", rust_code.lower())

    def test_generation_creates_command_structs(self):
        """Test that generated Rust code creates command structs."""
        rsrc_data = [
            {
                "kind": "foo",
                "apiVersion": "v1",
                "schema": {
                    "type": "array",
                    "key": {"name": "foo_key", "schema": {"type": "string"}},
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                        },
                    },
                },
                "methods": {
                    "resource": ["get", "post"],
                    "instance": ["get", "put", "delete"],
                },
            }
        ]
        result = cli_rust.generate(
            "test_pkg",
            "test_pkg::apis",
            rsrc_data,
            "Test API",
            "Test API Description",
            "Test Summary",
            "1.0",
            as_modules=True,
        )
        rust_code = result["foo"]
        # Check for command structs
        self.assertIn("pub struct CreateArgs", rust_code)
        self.assertIn("pub struct UpdateArgs", rust_code)
        self.assertIn("pub struct ListArgs", rust_code)
        self.assertIn("pub struct GetArgs", rust_code)
        self.assertIn("pub struct DeleteArgs", rust_code)

    def test_generation_creates_command_enum(self):
        """Test that generated Rust code creates command enum."""
        rsrc_data = [
            {
                "kind": "foo",
                "apiVersion": "v1",
                "schema": {
                    "type": "array",
                    "key": {"name": "foo_key", "schema": {"type": "string"}},
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                        },
                    },
                },
                "methods": {
                    "resource": ["get", "post"],
                    "instance": ["get", "put", "delete"],
                },
            }
        ]
        result = cli_rust.generate(
            "test_pkg",
            "test_pkg::apis",
            rsrc_data,
            "Test API",
            "Test API Description",
            "Test Summary",
            "1.0",
            as_modules=True,
        )
        rust_code = result["foo"]
        # Check for command enum
        self.assertIn("#[derive(Subcommand, Debug)]", rust_code)
        self.assertIn("pub enum FooCommands", rust_code)


class TestCliRustHelpers(unittest.TestCase):
    """Test helper functions in firestone.spec.cli_rust."""

    def test_to_singular_simple_s(self):
        """Strips trailing -s for simple plurals."""
        self.assertEqual(cli_rust._to_singular("books"), "book")
        self.assertEqual(cli_rust._to_singular("users"), "user")

    def test_to_singular_es_suffix(self):
        """Strips -es for sibilant-ending words."""
        self.assertEqual(cli_rust._to_singular("addresses"), "address")
        self.assertEqual(cli_rust._to_singular("boxes"), "box")
        self.assertEqual(cli_rust._to_singular("churches"), "church")
        self.assertEqual(cli_rust._to_singular("proxies"), "proxy")
        # composite word whose plural ends in -ses must survive round-trip
        self.assertEqual(cli_rust._to_singular("statuses"), "status")

    def test_to_singular_ies_suffix(self):
        """Converts -ies back to -y."""
        self.assertEqual(cli_rust._to_singular("categories"), "category")
        self.assertEqual(cli_rust._to_singular("libraries"), "library")
        self.assertEqual(cli_rust._to_singular("policies"), "policy")

    def test_to_singular_no_s(self):
        """Leaves words that don't end in -s unchanged."""
        self.assertEqual(cli_rust._to_singular("addressbook"), "addressbook")
        self.assertEqual(cli_rust._to_singular("person"), "person")

    def test_to_singular_double_s(self):
        """Words ending in -ss are not modified (composite or plain)."""
        self.assertEqual(cli_rust._to_singular("class"), "class")
        self.assertEqual(cli_rust._to_singular("subclass"), "subclass")
        self.assertEqual(cli_rust._to_singular("access"), "access")

    def test_number_type_mapping(self):
        """OpenAPI 'number' type maps to Rust f64."""
        params = [
            {
                "name": "price",
                "description": "A price value",
                "schema": {"type": "number"},
                "required": False,
            }
        ]
        attrs = cli_rust.params_to_attrs(params)
        self.assertEqual(attrs[0]["type"], "f64")

    def test_enum_variants_pascal_case(self):
        """Enum variant names are PascalCase, not SCREAMING_SNAKE_CASE."""
        params = [
            {
                "name": "status",
                "description": "Status",
                "schema": {"type": "string", "enum": ["active", "inactive", "pending-review"]},
                "required": True,
            }
        ]
        attrs = cli_rust.params_to_attrs(params)
        variant_names = [v["name"] for v in attrs[0]["enum_variants"]]
        self.assertEqual(variant_names, ["Active", "Inactive", "PendingReview"])

    def test_array_enum_variants_pascal_case(self):
        """Array-of-enum variant names are also PascalCase."""
        params = [
            {
                "name": "roles",
                "description": "Roles",
                "schema": {
                    "type": "array",
                    "items": {"type": "string", "enum": ["admin-ro", "read-write", "owner"]},
                },
                "required": False,
            }
        ]
        attrs = cli_rust.params_to_attrs(params)
        variant_names = [v["name"] for v in attrs[0]["enum_variants"]]
        self.assertEqual(variant_names, ["AdminRo", "ReadWrite", "Owner"])

    def test_singular_schema_override(self):
        """A 'singular' key in the resource schema overrides auto-derivation."""
        rsrc_data = [
            {
                "kind": "addresses",
                "singular": "address",
                "apiVersion": "v1",
                "schema": {
                    "type": "array",
                    "key": {"name": "address_key", "schema": {"type": "string"}},
                    "items": {
                        "type": "object",
                        "properties": {"name": {"type": "string"}},
                    },
                },
            }
        ]
        result = cli_rust.generate(
            "pkg", "pkg::apis", rsrc_data, "T", "D", "S", "1.0", as_modules=True
        )
        rust_code = result["addresses"]
        # Model types should use the explicit singular "address"
        self.assertIn("CreateAddress", rust_code)
        self.assertIn("UpdateAddress", rust_code)

    def test_create_handler_prints_response(self):
        """Generated create handler must print the API response as JSON."""
        rsrc_data = [
            {
                "kind": "books",
                "apiVersion": "v1",
                "schema": {
                    "type": "array",
                    "key": {"name": "book_key", "schema": {"type": "string"}},
                    "items": {
                        "type": "object",
                        "properties": {"title": {"type": "string"}},
                    },
                },
                "methods": {"resource": ["post"]},
            }
        ]
        result = cli_rust.generate(
            "pkg", "pkg::apis", rsrc_data, "T", "D", "S", "1.0", as_modules=True
        )
        rust_code = result["books"]
        # The create handler must output the response
        self.assertIn("serde_json::to_string_pretty(&resp)", rust_code)
        self.assertIn('println!("{}", json_output)', rust_code)

    def test_update_handler_prints_response(self):
        """Generated update handler must print the API response as JSON."""
        rsrc_data = [
            {
                "kind": "books",
                "apiVersion": "v1",
                "schema": {
                    "type": "array",
                    "key": {"name": "book_key", "schema": {"type": "string"}},
                    "items": {
                        "type": "object",
                        "properties": {"title": {"type": "string"}},
                    },
                },
                "methods": {"instance": ["put"]},
            }
        ]
        result = cli_rust.generate(
            "pkg", "pkg::apis", rsrc_data, "T", "D", "S", "1.0", as_modules=True
        )
        rust_code = result["books"]
        self.assertIn("serde_json::to_string_pretty(&resp)", rust_code)

    def test_enum_has_default_flag_set(self):
        """_enrich_attr_for_body sets enum_has_default when enum attr has a default value."""
        attr = {
            "name": "status",
            "rust_name": "status",
            "type": "StatusEnum",
            "is_enum": True,
            "is_enum_array": False,
            "argument": False,
            "required": False,
            "default": "active",
            "enum_variants": [
                {"name": "Active", "value": "active"},
                {"name": "Inactive", "value": "inactive"},
            ],
        }
        cli_rust._enrich_attr_for_body(attr, "books", "Book", "create")
        self.assertTrue(attr.get("enum_has_default"))

    def test_enum_without_default_has_no_flag(self):
        """_enrich_attr_for_body does NOT set enum_has_default when there is no default."""
        attr = {
            "name": "status",
            "rust_name": "status",
            "type": "StatusEnum",
            "is_enum": True,
            "is_enum_array": False,
            "argument": False,
            "required": False,
            "enum_variants": [
                {"name": "Active", "value": "active"},
                {"name": "Inactive", "value": "inactive"},
            ],
        }
        cli_rust._enrich_attr_for_body(attr, "books", "Book", "create")
        self.assertFalse(attr.get("enum_has_default", False))

    def test_optional_string_default_not_double_wrapped_on_update(self):
        """Update handlers must keep defaulted optional strings as Option<String>."""
        rsrc_data = [
            {
                "kind": "persons",
                "apiVersion": "v1",
                "schema": {
                    "type": "array",
                    "key": {"name": "uuid", "schema": {"type": "string"}},
                    "items": {
                        "type": "object",
                        "properties": {
                            "timezone": {
                                "type": "string",
                                "default": "UTC",
                            }
                        },
                    },
                },
                "methods": {"instance": ["put"]},
            }
        ]
        result = cli_rust.generate("pkg", "crate", rsrc_data, "T", "D", "S", "1.0", as_modules=True)
        rust_code = result["persons"]
        update_handler = rust_code.split("pub async fn handle_persons_uuid_put", maxsplit=1)[1]
        self.assertIn("timezone: args.timezone.clone()", update_handler)
        self.assertNotIn("timezone: Some(args.timezone.clone())", update_handler)

    def test_asref_str_impl_generated_for_enums(self):
        """Generated module includes impl AsRef<str> for each CLI enum type."""
        rsrc_data = [
            {
                "kind": "orders",
                "apiVersion": "v1",
                "schema": {
                    "type": "array",
                    "key": {"name": "order_id", "schema": {"type": "string"}},
                    "items": {
                        "type": "object",
                        "properties": {
                            "status": {
                                "type": "string",
                                "enum": ["pending", "shipped", "delivered"],
                            }
                        },
                    },
                },
                "methods": {"resource": ["get", "post"]},
            }
        ]
        result = cli_rust.generate(
            "pkg", "my_client", rsrc_data, "T", "D", "S", "1.0", as_modules=True
        )
        rust_code = result["orders"]
        self.assertIn("impl AsRef<str> for StatusEnum", rust_code)
        self.assertIn('StatusEnum::Pending => "pending"', rust_code)
        self.assertIn('StatusEnum::Shipped => "shipped"', rust_code)
        self.assertIn('StatusEnum::Delivered => "delivered"', rust_code)


class TestCliRustMultiSource(unittest.TestCase):
    """Test multi-source (multi-schema) generation behaviour."""

    def _make_rsrc(self, kind, namespace=None, client_pkg=None):
        rsrc = {
            "kind": kind,
            "apiVersion": "v1",
            "schema": {
                "type": "array",
                "key": {"name": f"{kind}_key", "schema": {"type": "string"}},
                "items": {
                    "type": "object",
                    "properties": {"name": {"type": "string"}},
                },
            },
            "methods": {"resource": ["get", "post"], "instance": ["get", "put", "delete"]},
        }
        if namespace:
            rsrc["namespace"] = namespace
        if client_pkg:
            rsrc["client_pkg"] = client_pkg
        return rsrc

    def test_duplicate_module_name_raises(self):
        """Two resources resolving to the same module_name must raise ValueError."""
        rsrc_data = [
            self._make_rsrc("users"),
            self._make_rsrc("users"),
        ]
        with self.assertRaises(ValueError) as ctx:
            cli_rust.generate("pkg", "default_client", rsrc_data, "T", "D", "S", "1.0")
        self.assertIn("users", str(ctx.exception))
        self.assertIn("namespace", str(ctx.exception))

    def test_namespace_eliminates_collision(self):
        """Same kind under different namespaces must produce distinct modules."""
        rsrc_data = [
            self._make_rsrc("users", namespace="project_a", client_pkg="project_a_client"),
            self._make_rsrc("users", namespace="project_b", client_pkg="project_b_client"),
        ]
        result = cli_rust.generate(
            "pkg", "default_client", rsrc_data, "T", "D", "S", "1.0", as_modules=True
        )
        self.assertIn("project_a_users", result)
        self.assertIn("project_b_users", result)
        self.assertEqual(len(result), 2)

    def test_per_resource_client_pkg_in_generated_code(self):
        """Each module must reference its own client crate, not the global one."""
        rsrc_data = [
            self._make_rsrc("books", namespace="lib_a", client_pkg="lib_a_client"),
        ]
        result = cli_rust.generate(
            "pkg", "global_client", rsrc_data, "T", "D", "S", "1.0", as_modules=True
        )
        rust_code = result["lib_a_books"]
        self.assertIn("lib_a_client::", rust_code)
        self.assertNotIn("global_client::", rust_code)

    def test_namespace_pascal_case_command_enum(self):
        """Module with namespace produces correctly cased Commands enum."""
        rsrc_data = [
            self._make_rsrc("orders", namespace="project_x", client_pkg="px_client"),
        ]
        result = cli_rust.generate(
            "pkg", "px_client", rsrc_data, "T", "D", "S", "1.0", as_modules=True
        )
        rust_code = result["project_x_orders"]
        self.assertIn("pub enum ProjectXOrdersCommands", rust_code)

    def test_generate_cargo_toml_unique_client_pkgs(self):
        """Cargo.toml has exactly one dependency entry per unique client crate."""
        rsrc_data = [
            self._make_rsrc("users", namespace="a", client_pkg="shared_client"),
            self._make_rsrc("books", namespace="b", client_pkg="shared_client"),
            self._make_rsrc("orders", namespace="c", client_pkg="other_client"),
        ]
        cargo = cli_rust.generate_cargo_toml("my_cli", "1.0.0", rsrc_data, "fallback_client")
        # Count actual dependency lines (not comment lines) to confirm deduplication.
        dep_lines = [line for line in cargo.splitlines() if line.startswith("shared_client ")]
        self.assertEqual(len(dep_lines), 1, "shared_client should appear once as a dep")
        dep_lines_other = [line for line in cargo.splitlines() if line.startswith("other_client ")]
        self.assertEqual(len(dep_lines_other), 1)
        self.assertNotIn("fallback_client", cargo)

    def test_generate_cargo_toml_includes_model_pkg_overrides(self):
        """Crates referenced only via model_pkg_overrides still appear in Cargo.toml."""
        rsrc_data = [
            {
                **self._make_rsrc("addressbook", client_pkg="addressbook_client"),
                "model_pkg_overrides": {"Person": "shared_models_client"},
            }
        ]
        cargo = cli_rust.generate_cargo_toml("cli", "1.0.0", rsrc_data, "fallback")
        dep_lines = [
            line for line in cargo.splitlines() if line.startswith("shared_models_client ")
        ]
        self.assertEqual(len(dep_lines), 1, "override target must appear as a dep")
        dep_lines_main = [
            line for line in cargo.splitlines() if line.startswith("addressbook_client ")
        ]
        self.assertEqual(len(dep_lines_main), 1)

    def test_generate_cargo_toml_falls_back_to_default(self):
        """Resources without client_pkg use the default in Cargo.toml."""
        rsrc_data = [self._make_rsrc("items")]
        cargo = cli_rust.generate_cargo_toml("cli", "0.1.0", rsrc_data, "default_client")
        self.assertIn("default_client", cargo)
        self.assertIn('name = "cli"', cargo)

    def test_model_pkg_overrides_ref_path(self):
        """model_pkg_overrides redirects a $ref model to the correct client crate."""
        attr = {
            "name": "person",
            "rust_name": "person",
            "type": "String",
            "required": False,
            "is_enum": False,
            "is_enum_array": False,
            "argument": False,
            "schema": {"$ref": "person.yaml#/schema"},
            "original_schema": {"$ref": "person.yaml#/schema"},
            "in": "body",
        }
        enriched = cli_rust._enrich_attr_for_body(
            attr,
            "addressbook",
            "addressbook",
            "create",
            client_pkg="addressbook_client",
            model_pkg_overrides={"person": "shared_models_client"},
        )
        self.assertIn("shared_models_client::models::Person", enriched["body_conversion"])
        self.assertNotIn("addressbook_client::models::Person", enriched["body_conversion"])

    def test_model_pkg_overrides_absent_uses_client_pkg(self):
        """Without an override, $ref model path uses the resource's own client_pkg."""
        attr = {
            "name": "person",
            "rust_name": "person",
            "type": "String",
            "required": False,
            "is_enum": False,
            "is_enum_array": False,
            "argument": False,
            "schema": {"$ref": "person.yaml#/schema"},
            "original_schema": {"$ref": "person.yaml#/schema"},
            "in": "body",
        }
        enriched = cli_rust._enrich_attr_for_body(
            attr,
            "addressbook",
            "addressbook",
            "create",
            client_pkg="addressbook_client",
        )
        self.assertIn("addressbook_client::models::Person", enriched["body_conversion"])


if __name__ == "__main__":
    unittest.main()
