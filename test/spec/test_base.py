"""
Test the firestone.spec.openapi module.
"""
import unittest

from firestone.spec import _base as spec_base


# pylint: disable=duplicate-code
class TestOpenAPIGetOpIs(unittest.TestCase):
    """Test all aspects of firestone.spec._base.get_opid"""

    def test_get_opid_correct_return(self):
        """Test firestone.spec.spec_base.get_opid returns correct opid."""

        opid = spec_base.get_opid("/foo/{bar}", "get")
        self.assertEqual(opid, "foo_bar_get")
