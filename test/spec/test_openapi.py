"""
Test the firestone.spec.openapi module.
"""

import http.client

import unittest
from unittest import mock

from firestone.spec import _base as spec_base
from firestone.spec import openapi


# pylint: disable=duplicate-code
class TestOpenAPIGetResponses(unittest.TestCase):
    """Test all aspects of firestone.spec.openapi.get_responses"""

    def test_head(self):
        """Test firestone.spec.openapi.get_responses() HEAD."""
        responses = openapi.get_responses(
            "head",
            None,
            None,
            None,
            None,
            None,
        )
        self.assertIsNotNone(responses)

    def test_get_comp_name(self):
        """Test firestone.spec.openapi.get_responses() 'get' with comp name."""
        responses = openapi.get_responses(
            "get",
            {"type": "object", "properties": {"foo": {"type": "string"}}},
            "application/json",
            comp_name="bar",
        )

        self.assertIsNotNone(responses)
        self.assertIsInstance(responses, dict)
        self.assertIn(http.client.OK, responses)
        self.assertIn("description", responses[http.client.OK])
        self.assertEqual(
            responses[http.client.OK]["content"]["application/json"]["schema"],
            {"$ref": "#/components/schemas/bar"},
        )

    def test_post_comp_name(self):
        """Test firestone.spec.openapi.get_responses() 'post' with comp name."""
        responses = openapi.get_responses(
            "post",
            {"type": "object", "properties": {"foo": {"type": "string"}}},
            "application/json",
            comp_name="bar",
        )

        self.assertIsNotNone(responses)
        self.assertIsInstance(responses, dict)
        self.assertNotIn(http.client.OK, responses)
        self.assertIn(http.client.CREATED, responses)
        self.assertIn("description", responses[http.client.CREATED])
        self.assertEqual(
            responses[http.client.CREATED]["content"]["application/json"]["schema"],
            {"$ref": "#/components/schemas/bar"},
        )

    def test_get_attr_name(self):
        """Test firestone.spec.openapi.get_responses() 'get' with attr name."""
        responses = openapi.get_responses(
            "get",
            {"type": "object", "properties": {"foo": {"type": "string"}}},
            "application/json",
            comp_name="bar",
            attr_name="baz",
        )

        self.assertIsNotNone(responses)
        self.assertIsInstance(responses, dict)
        self.assertEqual(
            responses[http.client.OK]["content"]["application/json"]["schema"],
            {"type": "object", "properties": {"foo": {"type": "string"}}},
        )

    def test_get_attr_name_is_list(self):
        """Test firestone.spec.openapi.get_responses() 'get' with attr name and is_list=True."""
        responses = openapi.get_responses(
            "get",
            {"type": "object", "properties": {"foo": {"type": "string"}}},
            "application/json",
            comp_name="bar",
            attr_name="baz",
            is_list=True,
        )

        self.assertIsNotNone(responses)
        self.assertIsInstance(responses, dict)
        self.assertEqual(
            responses[http.client.OK]["content"]["application/json"]["schema"],
            {"type": "object", "properties": {"foo": {"type": "string"}}},
        )


class TestOpenAPIGetMethodOp(unittest.TestCase):
    """Test all aspects of firestone.spec.openapi.get_method_op"""

    @mock.patch("firestone.spec.openapi.get_responses", return_value={})
    def test_no_desc(self, resps_mock):
        """Test firestone.spec.openapi.test() no desc."""
        method_op = openapi.get_method_op(
            "/foo",
            "get",
            {"type": "object", "properties": {"foo": {"type": "string"}}},
            desc=None,
        )
        self.assertIsNotNone(method_op)
        self.assertIsInstance(method_op, dict)

        self.assertEqual(method_op["description"], "get operation for /foo")

        resps_mock.assert_called_with(
            "get",
            {"type": "object", "properties": {"foo": {"type": "string"}}},
            "application/json",
            comp_name=None,
            attr_name=None,
            is_list=None,
        )

    @mock.patch("firestone.spec.openapi.get_responses", return_value={})
    def test_desc(self, _resps_mock):
        """Test firestone.spec.openapi.test() with desc."""
        method_op = openapi.get_method_op(
            "/foo",
            "get",
            {"type": "object", "properties": {"foo": {"type": "string"}}},
            desc="Foo bar",
        )
        self.assertIsNotNone(method_op)
        self.assertIsInstance(method_op, dict)

        self.assertEqual(method_op["description"], "Foo bar")

    @mock.patch("firestone.spec.openapi.get_responses", return_value={})
    def test_post(self, _resps_mock):
        """Test firestone.spec.openapi.test() with post method."""
        method_op = openapi.get_method_op(
            "/foo",
            "post",
            {"type": "object", "properties": {"foo": {"type": "string"}}},
            desc="Foo bar",
        )
        self.assertIsNotNone(method_op)
        self.assertIsInstance(method_op, dict)

        self.assertIn("requestBody", method_op)


class TestOpenAPIGetParams(unittest.TestCase):
    """Test all aspects of firestone.spec.openapi.get_params"""

    def test_no_query(self):
        """Test firestone.spec.openapi.test_get_params() no query_params."""
        params = openapi.get_params(
            "/foo",
            "get",
            {
                "type": "array",
                "items": {"type": "object", "properties": {"foo": {"type": "string"}}},
            },
        )

        self.assertIsNotNone(params)
        self.assertEqual(params, [])

    def test_with_path_name(self):
        """Test firestone.spec.openapi.test_get_params() with path_name."""
        params = openapi.get_params(
            "/foo/{foo}",
            "get",
            {
                "type": "array",
                "items": {"type": "object", "properties": {"foo": {"type": "string"}}},
            },
            keys=[
                {
                    "name": "foo",
                    "schema": {
                        "type": "string",
                    },
                }
            ],
        )

        self.assertIsNotNone(params)
        self.assertEqual(len(params), 1)
        self.assertEqual(
            params,
            [
                {
                    "name": "foo",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "string"},
                }
            ],
        )

    def test_with_path_name_schema(self):
        """Test firestone.spec.openapi.test_get_params() with path_name and param_schema."""
        params = openapi.get_params(
            "/foo/{foo}",
            "get",
            {
                "type": "array",
                "items": {"type": "object", "properties": {"foo": {"type": "string"}}},
            },
            param_schema={"type": "integer"},
            keys=[
                {
                    "name": "foo",
                    "schema": {
                        "type": "string",
                    },
                }
            ],
        )

        self.assertIsNotNone(params)
        self.assertEqual(len(params), 1)
        self.assertEqual(
            params,
            [
                {
                    "name": "foo",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "integer"},
                }
            ],
        )

    def test_with_query_params(self):
        """Test firestone.spec.openapi.test_get_params() with query_params, default False."""
        params = openapi.get_params(
            "/foo/{foo}",
            "get",
            {
                "type": "array",
                "query_params": [
                    {
                        "name": "foo",
                        "description": "Filter by foo name",
                        "schema": {"type": "string"},
                        "methods": ["get"],
                    }
                ],
            },
        )

        self.assertIsNotNone(params)
        self.assertEqual(len(params), 1)
        self.assertEqual(
            params,
            [
                {
                    "name": "foo",
                    "description": "Filter by foo name",
                    "in": "query",
                    "required": False,
                    "schema": {"type": "string"},
                }
            ],
        )

    def test_with_query_params_meth(self):
        """Test firestone.spec.openapi.test_get_params() with query_params and method skipping."""
        params = openapi.get_params(
            "/foo/{foo}",
            "post",
            {
                "type": "array",
                "query_params": [
                    {
                        "name": "foo",
                        "description": "Filter by foo name",
                        "schema": {"type": "string"},
                        "methods": ["get"],
                    }
                ],
            },
        )

        self.assertIsNotNone(params)
        self.assertEqual(params, [])

    def test_with_query_params_true(self):
        """Test firestone.spec.openapi.test_get_params() with query_params, with required=True."""
        params = openapi.get_params(
            "/foo/{foo}",
            "get",
            {
                "type": "array",
                "query_params": [
                    {
                        "name": "foo",
                        "description": "Filter by foo name",
                        "required": True,
                        "schema": {"type": "string"},
                        "methods": ["get"],
                    }
                ],
            },
        )

        self.assertIsNotNone(params)
        self.assertEqual(len(params), 1)
        self.assertEqual(
            params,
            [
                {
                    "name": "foo",
                    "description": "Filter by foo name",
                    "in": "query",
                    "required": True,
                    "schema": {"type": "string"},
                }
            ],
        )


class TestOpenAPIAddResourceMethods(unittest.TestCase):
    """Test all aspects of firestone.spec.openapi.add_resource_methods"""

    @mock.patch("firestone.spec.openapi.get_method_op", return_value={})
    @mock.patch("firestone.spec.openapi.get_params", return_value={})
    def test_no_default_params(self, _params_mock, _method_op_mock):
        """Test no default_query_params."""
        paths = {}
        openapi.add_resource_methods(
            "foo",
            {
                "type": "array",
                "items": {"type": "object", "properties": {"foo": {"type": "string"}}},
            },
            "/",
            paths,
        )

        self.assertIsNotNone(paths)
        self.assertIsInstance(paths["/"], dict)

        self.assertIn("delete", paths["/"])
        self.assertIn("get", paths["/"])
        self.assertIn("head", paths["/"])
        self.assertIn("patch", paths["/"])
        self.assertIn("post", paths["/"])

    @mock.patch("firestone.spec.openapi.get_method_op", return_value={})
    @mock.patch("firestone.spec.openapi.get_params", return_value={})
    def test_with_methods(self, _params_mock, _method_op_mock):
        """Test with methods."""
        paths = {}
        openapi.add_resource_methods(
            "foo",
            {
                "type": "array",
                "items": {"type": "object", "properties": {"foo": {"type": "string"}}},
            },
            "/",
            paths,
            methods=["get"],
        )

        self.assertIsNotNone(paths)
        self.assertIsInstance(paths["/"], dict)

        self.assertIn("get", paths["/"])
        self.assertNotIn("delete", paths["/"])
        self.assertNotIn("head", paths["/"])
        self.assertNotIn("patch", paths["/"])
        self.assertNotIn("post", paths["/"])

    @mock.patch("firestone.spec.openapi.get_method_op", return_value={})
    @mock.patch("firestone.spec.openapi.get_params", return_value={})
    def test_tags(self, _params_mock, _method_op_mock):
        """Test tags exist."""
        paths = {}
        openapi.add_resource_methods(
            "foo",
            {
                "type": "array",
                "items": {"type": "object", "properties": {"foo": {"type": "string"}}},
            },
            "/",
            paths,
        )

        self.assertIsNotNone(paths)
        self.assertIsInstance(paths["/"], dict)
        self.assertIn("foo", paths["/"]["get"]["tags"])

    @mock.patch("firestone.spec.openapi.get_method_op", return_value={})
    @mock.patch("firestone.spec.openapi.get_params", return_value=[])
    def test_with_default_params(self, _params_mock, _method_op_mock):
        """Test tags exist."""
        paths = {}
        openapi.add_resource_methods(
            "foo",
            {
                "type": "array",
                "items": {"type": "object", "properties": {"foo": {"type": "string"}}},
            },
            "/",
            paths,
            default_query_params=[
                {
                    "name": "foo",
                    "description": "Limit the number of responses back",
                    "in": "params",
                    "schema": {"type": "integer"},
                }
            ],
        )

        self.assertIsNotNone(paths)
        self.assertIsInstance(paths["/"], dict)
        self.assertIn("parameters", paths["/"]["get"])


class TestOpenAPIAddInstanceMethods(unittest.TestCase):
    """Test all aspects of firestone.spec.openapi.add_instance_methods"""

    @mock.patch("firestone.spec.openapi.get_method_op", return_value={})
    @mock.patch("firestone.spec.openapi.get_params", return_value=[])
    def test_no_methods(self, _params_mock, _method_op_mock):
        """Test no methods."""
        paths = {}
        openapi.add_instance_methods(
            "foo",
            {
                "type": "array",
                "items": {"type": "object", "properties": {"foo": {"type": "string"}}},
            },
            "/foo/{foo_key}",
            paths,
        )

        self.assertIsNotNone(paths)
        self.assertIsInstance(paths["/foo/{foo_key}"], dict)

        self.assertIn("delete", paths["/foo/{foo_key}"])
        self.assertIn("get", paths["/foo/{foo_key}"])
        self.assertIn("head", paths["/foo/{foo_key}"])
        self.assertIn("patch", paths["/foo/{foo_key}"])
        self.assertIn("put", paths["/foo/{foo_key}"])

    @mock.patch("firestone.spec.openapi.get_method_op", return_value={})
    @mock.patch("firestone.spec.openapi.get_params", return_value=[])
    def test_with_methods(self, _params_mock, _method_op_mock):
        """Test with methods."""
        paths = {}
        openapi.add_instance_methods(
            "foo",
            {
                "type": "array",
                "items": {"type": "object", "properties": {"foo": {"type": "string"}}},
            },
            "/foo/{foo_key}",
            paths,
            methods=["get"],
        )

        self.assertIsNotNone(paths)
        self.assertIsInstance(paths["/foo/{foo_key}"], dict)

        self.assertIn("get", paths["/foo/{foo_key}"])
        self.assertNotIn("delete", paths["/foo/{foo_key}"])
        self.assertNotIn("head", paths["/foo/{foo_key}"])
        self.assertNotIn("patch", paths["/foo/{foo_key}"])
        self.assertNotIn("post", paths["/foo/{foo_key}"])

    @mock.patch("firestone.spec.openapi.get_method_op", return_value={})
    @mock.patch("firestone.spec.openapi.get_params", return_value=[])
    def test_tags(self, _params_mock, _method_op_mock):
        """Test tags exist."""
        paths = {}
        openapi.add_instance_methods(
            "foo",
            {
                "type": "array",
                "items": {"type": "object", "properties": {"foo": {"type": "string"}}},
            },
            "/foo/{foo_key}",
            paths,
        )

        self.assertIsNotNone(paths)
        self.assertIsInstance(paths["/foo/{foo_key}"], dict)
        self.assertIn("foo", paths["/foo/{foo_key}"]["get"]["tags"])


class TestOpenAPIAddInstanceAttrMethods(unittest.TestCase):
    """Test all aspects of firestone.spec.openapi.add_instance_attr_methods"""

    @mock.patch("firestone.spec.openapi.get_method_op", return_value={})
    @mock.patch("firestone.spec.openapi.get_params", return_value=[])
    def test_no_methods(self, _params_mock, _method_op_mock):
        """Test no methods."""
        paths = {}
        openapi.add_instance_attr_methods(
            "foo",
            {
                "type": "array",
                "items": {"type": "object", "properties": {"bar": {"type": "string"}}},
            },
            "/foo/{foo_key}",
            paths,
            components={"schemas": {}},
            methods={},
        )

        self.assertIsNotNone(paths)
        self.assertIsInstance(paths["/foo/{foo_key}/bar"], dict)

        self.assertIn("delete", paths["/foo/{foo_key}/bar"])
        self.assertIn("get", paths["/foo/{foo_key}/bar"])
        self.assertIn("head", paths["/foo/{foo_key}/bar"])
        self.assertIn("put", paths["/foo/{foo_key}/bar"])
        self.assertNotIn("patch", paths["/foo/{foo_key}/bar"])

    @mock.patch("firestone.spec.openapi.get_method_op", return_value={})
    @mock.patch("firestone.spec.openapi.get_params", return_value=[])
    def test_with_no_expose(self, _params_mock, _method_op_mock):
        """Test with expose=False."""
        paths = {}
        openapi.add_instance_attr_methods(
            "foo",
            {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {"bar": {"type": "string", "expose": False}},
                },
            },
            "/foo/{foo_key}",
            paths,
            methods={},
        )

        self.assertIsNotNone(paths)
        self.assertNotIn("/foo/{foo_key}/bar", paths)

    @mock.patch("firestone.spec.openapi.get_method_op", return_value={})
    @mock.patch("firestone.spec.openapi.get_params", return_value=[])
    def test_with_methods(self, _params_mock, _method_op_mock):
        """Test with methods."""
        paths = {}
        openapi.add_instance_attr_methods(
            "foo",
            {
                "type": "array",
                "items": {"type": "object", "properties": {"bar": {"type": "string"}}},
                "methods": ["get"],
            },
            "/foo/{foo_key}",
            paths,
            methods={"instance_attrs": ["get"]},
            components={"schemas": {}},
        )

        self.assertIsNotNone(paths)
        self.assertIsInstance(paths["/foo/{foo_key}/bar"], dict)

        self.assertIn("get", paths["/foo/{foo_key}/bar"])
        self.assertNotIn("delete", paths["/foo/{foo_key}/bar"])
        self.assertNotIn("head", paths["/foo/{foo_key}/bar"])
        self.assertNotIn("put", paths["/foo/{foo_key}/bar"])

    @mock.patch("firestone.spec.openapi.get_method_op", return_value={})
    @mock.patch("firestone.spec.openapi.get_params", return_value=[])
    @mock.patch("firestone.spec.openapi.get_paths")
    def test_with_items(self, _paths_mock, _params_mock, _method_op_mock):
        """Test with items, i.e. sub-resoure."""
        paths = {}
        openapi.add_instance_attr_methods(
            "foo",
            {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "bar": {"type": "string"},
                        "foobar": {
                            "schema": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "baz": {"type": "string"},
                                    },
                                },
                            },
                        },
                    },
                },
            },
            "/foo/{foo_key}",
            paths,
            components={"schemas": {}},
            methods={},
        )

        self.assertIsNotNone(paths)
        self.assertIsInstance(paths["/foo/{foo_key}/bar"], dict)
        self.assertIsInstance(paths["/foo/{foo_key}/foobar"], dict)

        self.assertIn("get", paths["/foo/{foo_key}/bar"])
        self.assertIn("get", paths["/foo/{foo_key}/foobar"])


class TestOpenAPIGetPaths(unittest.TestCase):
    """Test all aspects of firestone.spec.openapi.get_paths"""

    @mock.patch("firestone.spec.openapi.add_instance_methods")
    @mock.patch("firestone.spec.openapi.add_instance_attr_methods")
    def test_raise_exc(self, _inst_attr_meth_mock, _inst_meth_mock):
        """Test no paths."""
        with self.assertRaises(spec_base.SchemaMissingAttribute):
            paths = openapi.get_paths(
                "foo",
                {
                    "type": "array",
                    "items": {"type": "object", "properties": {"bar": {"type": "string"}}},
                },
                "/foo",
            )

            self.assertIsNotNone(paths)

    @mock.patch("firestone.spec.openapi.add_instance_methods")
    @mock.patch("firestone.spec.openapi.add_instance_attr_methods")
    def test_no_paths(self, inst_attr_meth_mock, _inst_meth_mock):
        """Test no paths."""
        paths = openapi.get_paths(
            "foo",
            {
                "type": "array",
                "key": {"name": "foo_key", "schema": {"type": "string"}},
                "items": {"type": "object", "properties": {"bar": {"type": "string"}}},
            },
            "/foo",
            keys=[{"name": "foo_key", "schema": {"type": "string"}}],
        )

        self.assertIsNotNone(paths)

        inst_attr_meth_mock.assert_called_with(
            "foo",
            {
                "type": "array",
                "key": {"name": "foo_key", "schema": {"type": "string"}},
                "items": {"type": "object", "properties": {"bar": {"type": "string"}}},
            },
            "/foo/{foo_key}",
            mock.ANY,
            methods={},
            keys=[{"name": "foo_key", "schema": {"type": "string"}}],
            default_query_params=None,
            components=None,
            orig_rsrc_name=None,
        )


class TestOpenAPIGenerate(unittest.TestCase):
    """Test all aspects of firestone.spec.openapi.generate"""

    def test_comp(self):
        """Test no paths."""
        spec = openapi.generate(
            [
                {
                    "kind": "foo",
                    "description": "Some foo resource",
                    "apiVersion": "1.0",
                    "schema": {
                        "type": "array",
                        "key": {"name": "foo_key", "schema": {"type": "string"}},
                        "items": {"type": "object", "properties": {"bar": {"type": "string"}}},
                    },
                }
            ],
            "Foo API",
            "Some Foo API",
            "Summary of Foo API",
            "1.0",
        )

        self.assertIsNotNone(spec)

        self.assertIn("components", spec)
        self.assertIn("Foo API", spec)
        self.assertIn("Some Foo API", spec)
        self.assertIn("/foo", spec)
        self.assertIn("/foo/{foo_key}", spec)

    def test_version_in(self):
        """Test version in path."""
        spec = openapi.generate(
            [
                {
                    "kind": "foo",
                    "description": "Some foo resource",
                    "apiVersion": "1.0",
                    "versionInPath": True,
                    "schema": {
                        "type": "array",
                        "key": {"name": "foo_key", "schema": {"type": "string"}},
                        "items": {"type": "object", "properties": {"bar": {"type": "string"}}},
                    },
                }
            ],
            "Foo API",
            "Some Foo API",
            "Summary of Foo API",
            "1.0",
        )

        self.assertIsNotNone(spec)

        self.assertIn("/v1.0/foo", spec)
        self.assertIn("/v1.0/foo/{foo_key}", spec)

    def test_descriptions(self):
        """Test method descriptions."""
        spec = openapi.generate(
            [
                {
                    "kind": "foo",
                    "description": "Some foo resource",
                    "apiVersion": "1.0",
                    "descriptions": {
                        "resource": {
                            "get": "The get method is fabulous",
                        },
                    },
                    "schema": {
                        "type": "array",
                        "key": {
                            "name": "foo_key",
                            "schema": {"type": "string"},
                        },
                        "items": {
                            "type": "object",
                            "properties": {"bar": {"type": "string"}},
                        },
                    },
                }
            ],
            "Foo API",
            "Some Foo API",
            "Summary of Foo API",
            "1.0",
        )
        self.assertIsNotNone(spec)

        self.assertIn("components", spec)
        self.assertIn("Foo API", spec)
        self.assertIn("Some Foo API", spec)
        self.assertIn("/foo", spec)
        self.assertIn("/foo/{foo_key}", spec)
        self.assertIn("The get method is fabulous", spec)
        self.assertIn("1.0", spec)


if __name__ == "__main__":
    unittest.main()
