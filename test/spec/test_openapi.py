"""
Test the firestone.spec.openapi module.
"""

import unittest

from firestone.spec import openapi


class OpenAPITest(unittest.TestCase):
    """Test all functions in firestone.spec.openapi."""

    def test_get_opid_correct_return(self):
        """Test firestone.spec.openapi.get_opid returns correct opid."""

        opid = openapi.get_opid("/foo/{bar}", "get")
        self.assertEqual(opid, "foo_bar_get")


if __name__ == '__main__':
    unittest.main()
