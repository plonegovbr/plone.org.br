from plonegovbr.portal import PACKAGE_NAME
from Products.GenericSetup.tool import SetupTool

import pytest


class TestSetupInstall:
    def test_addon_installed(self, installer):
        """Test if plonegovbr.portal is installed."""
        assert installer.is_product_installed(PACKAGE_NAME) is True

    def test_browserlayer(self, browser_layers):
        """Test that IBrowserLayer is registered."""
        from plonegovbr.portal.interfaces import IBrowserLayer

        assert IBrowserLayer in browser_layers

    def test_latest_version(self, profile_last_version):
        """Test latest version of default profile."""
        assert profile_last_version(f"{PACKAGE_NAME}:default") == "20250903001"


class TestSetupDependencies:
    @pytest.fixture(autouse=True)
    def _setup(self, portal_class):
        self.portal = portal_class
        self.setup_tool: SetupTool = portal_class.portal_setup

    @pytest.mark.parametrize(
        "profile",
        [
            "plone.restapi:default",
            "plone.volto:default",
            "kitconcept.voltolighttheme:default",
            "collective.volto.formsupport:default",
            "collective.casestudy:default",
            "plonegovbr.socialmedia:default",
        ],
    )
    def test_installed(self, profile: str):
        """Test if a profile is installed."""
        assert self.setup_tool.getLastVersionForProfile(profile) is not None
