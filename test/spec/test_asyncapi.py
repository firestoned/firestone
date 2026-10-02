"""
Test the firestone.spec.asyncapi module.
"""

import unittest

import yaml

from firestone.spec import asyncapi


def _resource():
    """A resource with resource and instance channels turned on."""
    return {
        "kind": "books",
        "apiVersion": "v1",
        "metadata": {"description": "Some books"},
        "asyncapi": {
            "servers": {"dev": {"url": "ws://localhost", "protocol": "ws"}},
            "channels": {"resources": True, "instances": True},
        },
        "default_query_params": [
            {"name": "limit", "description": "Limit the results", "schema": {"type": "integer"}},
        ],
        "schema": {
            "type": "array",
            "key": {
                "name": "book_id",
                "description": "A unique identifier for a book",
                "schema": {"type": "string"},
            },
            "items": {
                "type": "object",
                "properties": {"title": {"type": "string"}},
            },
        },
    }


class TestAsyncAPIGenerate(unittest.TestCase):
    """Test all aspects of firestone.spec.asyncapi.generate"""

    def _generate(self):
        return yaml.safe_load(
            asyncapi.generate([_resource()], "Books API", "Some books API", "Books", "1.0")
        )

    def test_channels_named_after_kind(self):
        """A resource is named by its kind, it has no top level 'name'."""
        spec = self._generate()

        self.assertIn("/books", spec["channels"])
        self.assertIn("/books/{book_id}", spec["channels"])
        message = spec["channels"]["/books"]["subscribe"]["message"]
        self.assertEqual(message["name"], "books")

    def test_valid_document(self):
        """The rendered document parses, with channels at the top level."""
        spec = self._generate()

        self.assertEqual(
            list(spec),
            ["asyncapi", "defaultContentType", "info", "servers", "components", "channels"],
        )
        self.assertIn("books", spec["components"]["schemas"])
