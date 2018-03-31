# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from taiwananthro.content.testing import TAIWANANTHRO_CONTENT_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that taiwananthro.content is properly installed."""

    layer = TAIWANANTHRO_CONTENT_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if taiwananthro.content is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'taiwananthro.content'))

    def test_browserlayer(self):
        """Test that ITaiwananthroContentLayer is registered."""
        from taiwananthro.content.interfaces import (
            ITaiwananthroContentLayer)
        from plone.browserlayer import utils
        self.assertIn(ITaiwananthroContentLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = TAIWANANTHRO_CONTENT_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['taiwananthro.content'])

    def test_product_uninstalled(self):
        """Test if taiwananthro.content is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'taiwananthro.content'))

    def test_browserlayer_removed(self):
        """Test that ITaiwananthroContentLayer is removed."""
        from taiwananthro.content.interfaces import \
            ITaiwananthroContentLayer
        from plone.browserlayer import utils
        self.assertNotIn(ITaiwananthroContentLayer, utils.registered_layers())
