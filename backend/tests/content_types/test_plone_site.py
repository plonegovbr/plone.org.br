"""Tests for the site root FTI."""

from . import PLONE_SITE_BEHAVIORS
from plone.dexterity.fti import DexterityFTI

import pytest


@pytest.fixture(scope="class")
def portal_type() -> str:
    """Return the portal type under test."""
    return "Plone Site"


class TestPloneSiteFTI:
    """The site root carries the behaviors this policy package enables."""

    @pytest.fixture(autouse=True)
    def _setup(self, portal, portal_type, get_fti) -> None:
        """Bind the site and the FTI of the type under test to the instance."""
        self.portal = portal
        self.portal_type = portal_type
        self.fti: DexterityFTI = get_fti(portal_type)

    @pytest.mark.parametrize(
        "attr,expected",
        [
            ("title", "Plone Site"),
            ("klass", "Products.CMFPlone.Portal.PloneSite"),
            ("global_allow", False),
        ],
    )
    def test_fti(self, attr: str, expected):
        """Test FTI values."""
        fti = self.fti

        assert isinstance(fti, DexterityFTI)
        assert getattr(fti, attr) == expected

    @pytest.mark.parametrize("idx,behavior", enumerate(PLONE_SITE_BEHAVIORS))
    def test_behaviors(self, idx: int, behavior: str):
        """Test behaviors are present and in correct order."""
        assert self.fti.behaviors[idx] == behavior

    def test_no_extra_behaviors(self):
        """A behavior appended past the last expected one still has to be seen.

        The parametrized test above indexes into the list, so it is blind to
        anything a dependency adds at the end.
        """
        assert len(self.fti.behaviors) == len(PLONE_SITE_BEHAVIORS)
