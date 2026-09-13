# pylint: disable=duplicate-code
"""
Test the firestone.spec.cli module.
"""

import ast
import unittest

from firestone.spec import cli


def _resource() -> dict:
    """Get a resource with a boolean property, which needs a click flag pair."""
    return {
        "kind": "things",
        "apiVersion": "v1",
        "schema": {
            "type": "array",
            "key": {"name": "thing_key", "schema": {"type": "string"}},
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "The name"},
                    "is_valid": {"type": "boolean", "description": "Valid or not"},
                },
            },
        },
        "methods": {"resource": ["get", "post"], "instance": ["get", "put", "delete"]},
    }


class TestCliBooleans(unittest.TestCase):
    """Test how the generated python CLI declares a boolean option."""

    def test_single_file_output_parses(self):
        """The generated CLI has to be importable, which a bad option breaks.

        A flag pair written without its '/' becomes one option named
        --is-valid--no-is-valid, which click turns into an 'is_valid__no_is_valid'
        parameter, and the handler then rejects at runtime.
        """
        generated = cli.generate(
            "pkg", "pkg.client", [_resource()], "Title", "Desc", "Summary", "1.0", False
        )

        ast.parse(generated)

    def test_flag_pair_is_declared(self):
        """A boolean is a --x/--no-x pair, so it can be turned off as well as on."""
        generated = cli.generate(
            "pkg", "pkg.client", [_resource()], "Title", "Desc", "Summary", "1.0", False
        )

        self.assertIn('"--is-valid/--no-is-valid"', generated)
        self.assertNotIn('"--is-valid--no-is-valid"', generated)

    def test_modules_output_parses(self):
        """The per-module output has to be importable too."""
        modules = cli.generate(
            "pkg", "pkg.client", [_resource()], "Title", "Desc", "Summary", "1.0", True
        )

        for name, content in modules.items():
            ast.parse(content, filename=f"{name}.py")

    def test_both_outputs_agree(self):
        """The single file and the modules declare the option the same way."""
        single = cli.generate(
            "pkg", "pkg.client", [_resource()], "Title", "Desc", "Summary", "1.0", False
        )
        modules = cli.generate(
            "pkg", "pkg.client", [_resource()], "Title", "Desc", "Summary", "1.0", True
        )

        self.assertIn('"--is-valid/--no-is-valid"', single)
        self.assertIn('"--is-valid/--no-is-valid"', modules["things"])


if __name__ == "__main__":
    unittest.main()
