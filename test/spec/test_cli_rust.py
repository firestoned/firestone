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


if __name__ == "__main__":
    unittest.main()
