"""test_base module."""


import unittest

from orm.services.audit_trail_manager.audit_server.services.base import Error


class Test(unittest.TestCase):
    """test base class."""

    def test_init_Error(self):
        """Test that init of Error succeeded."""
        Error("test")
        pass
