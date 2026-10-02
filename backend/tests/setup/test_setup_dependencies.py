"""Tests for what the default profile pulls into a fresh site."""

from . import GLOBALLY_ALLOWED_TYPES
from . import INSTALLED_PROFILES
from . import NOT_INSTALLED_PROFILES
from . import PORTAL_TYPES
from . import VERSIONABLE_TYPES
from plone.dexterity.fti import DexterityFTI
from Products.CMFPlone.TypesTool import TypesTool
from Products.GenericSetup.tool import SetupTool

import pytest


class TestSetupDependencies:
    """Dependency profiles, and the ones that must stay out."""

    @pytest.fixture(autouse=True)
    def _setup(self, portal) -> None:
        """Bind the site and the setup tool to the instance."""
        self.portal = portal
        self.setup_tool: SetupTool = portal.portal_setup

    @pytest.mark.parametrize("profile", INSTALLED_PROFILES)
    def test_installed(self, profile: str):
        """Test if a profile is installed."""
        assert self.setup_tool.getLastVersionForProfile(profile) != "unknown"

    @pytest.mark.parametrize("profile", NOT_INSTALLED_PROFILES)
    def test_uninstalled(self, profile: str):
        """Test if a profile is not installed."""
        assert self.setup_tool.getLastVersionForProfile(profile) == "unknown"


class TestPortalTypes:
    """Content types available in a fresh site."""

    @pytest.fixture(autouse=True)
    def _setup(self, portal) -> None:
        """Bind the site and the types tool to the instance."""
        self.portal = portal
        self.types_tool: TypesTool = portal.portal_types

    @pytest.mark.parametrize("portal_type,title,klass", PORTAL_TYPES)
    def test_portal_type(self, portal_type: str, title: str, klass: str):
        """Test if a portal_type is installed."""
        fti = self.types_tool.getTypeInfo(portal_type)

        assert isinstance(fti, DexterityFTI)
        assert fti.title == title
        assert fti.klass == klass

    @pytest.mark.parametrize("portal_type", GLOBALLY_ALLOWED_TYPES)
    def test_global_allow(self, portal_type: str):
        """Test a type can be added anywhere in the site."""
        assert self.types_tool.getTypeInfo(portal_type).global_allow is True

    def test_no_unexpected_portal_types(self):
        """No add-on registered a type we did not account for.

        ``TempFolder`` is a Zope internal, not a Dexterity type, so it is
        excluded rather than listed in :data:`PORTAL_TYPES`.
        """
        expected = {portal_type for portal_type, _, _ in PORTAL_TYPES}
        installed = set(self.types_tool.objectIds()) - {"TempFolder"}

        assert installed == expected


class TestVersioning:
    """Versioning policies registered in ``portal_repository``."""

    @pytest.mark.parametrize("portal_type", VERSIONABLE_TYPES)
    def test_versionable(self, portal_type: str, versionable_content_types: list[str]):
        """Test the type is registered in portal_repository."""
        assert portal_type in versionable_content_types
