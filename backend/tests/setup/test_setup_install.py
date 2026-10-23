"""Tests for the installation of the plonegovbr.site add-on."""

from . import DEFAULT_PROFILE
from . import DEFAULT_PROFILE_VERSION
from . import HIDDEN_PRODUCTS
from . import HIDDEN_PROFILES
from plone.base.interfaces.installable import INonInstallable
from plonegovbr.site import PACKAGE_NAME
from plonegovbr.site.interfaces import IBrowserLayer
from zope.component import getUtility

import pytest


class TestSetupInstall:
    """The add-on is installed and registers what it declares."""

    @pytest.fixture(autouse=True)
    def _setup(self, portal) -> None:
        """Bind the site to the instance."""
        self.portal = portal

    def test_addon_installed(self, installer):
        """Test if plonegovbr.site is installed."""
        assert installer.is_product_installed(PACKAGE_NAME) is True

    def test_browserlayer(self, browser_layers):
        """Test that IBrowserLayer is registered."""
        assert IBrowserLayer in browser_layers

    def test_latest_version(self, profile_last_version):
        """Test latest version of default profile."""
        assert profile_last_version(DEFAULT_PROFILE) == DEFAULT_PROFILE_VERSION


class TestHiddenProfiles:
    """The ``HiddenProfiles`` utility keeps internals out of the control panel."""

    @pytest.fixture(autouse=True)
    def _setup(self, portal) -> None:
        """Look the utility up the way the add-ons control panel does."""
        self.portal = portal
        self.utility = getUtility(INonInstallable, name=PACKAGE_NAME)

    def test_non_installable_profiles(self):
        """Test exactly which profiles are hidden from the control panel.

        Asserted as a whole rather than one parametrized case per profile:
        :data:`HIDDEN_PROFILES` is empty, and an empty ``parametrize`` skips
        the test instead of failing it.
        """
        assert list(self.utility.getNonInstallableProfiles()) == list(HIDDEN_PROFILES)

    @pytest.mark.parametrize("product", HIDDEN_PRODUCTS)
    def test_non_installable_product(self, product: str):
        """Test a product is hidden from site creation and quickinstaller."""
        assert product in self.utility.getNonInstallableProducts()

    def test_default_profile_is_visible(self):
        """The profile the site is built from must stay installable."""
        assert DEFAULT_PROFILE not in self.utility.getNonInstallableProfiles()


class TestActions:
    """Portal actions configured by ``profiles/default/actions.xml``."""

    @pytest.fixture(autouse=True)
    def _setup(self, portal) -> None:
        """Bind the ``portal_tabs`` action category to the instance."""
        self.portal = portal
        self.portal_tabs = portal.portal_actions["portal_tabs"]

    def test_index_html_not_visible(self):
        """The Home tab is hidden: Volto renders its own navigation root."""
        assert self.portal_tabs["index_html"].visible is False
