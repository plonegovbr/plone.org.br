"""Tests for the UserProfile FTI and its relation to Organizations."""

from collections.abc import Generator
from collective.casestudy.utils.relations import case_studies_for_organization
from pas.plugins.identity.api import profile as profile_api
from plone import api
from plone.dexterity.content import DexterityContent
from plone.dexterity.fti import DexterityFTI
from plonegovbr.site.behaviors.affiliations import IAffiliations

import pytest


USER_PROFILE_BEHAVIORS = (
    "pas.plugins.identity.profile_details",
    "pas.plugins.identity.email_addresses",
    "pas.plugins.identity.group_membership",
    "plone.shortname",
    "plone.versioning",
    "plonegovbr.socialmedia.links",
    "plonegovbr.site.affiliations",
)


class TestUserProfileFTI:
    """The policy package adds the affiliations behavior to UserProfile."""

    @pytest.fixture(autouse=True)
    def _setup(self, portal, get_fti) -> None:
        """Bind the site and the UserProfile FTI to the instance."""
        self.portal = portal
        self.fti: DexterityFTI = get_fti("UserProfile")

    @pytest.mark.parametrize("idx,behavior", enumerate(USER_PROFILE_BEHAVIORS))
    def test_behaviors(self, idx: int, behavior: str):
        """Test behaviors are present and in correct order."""
        assert self.fti.behaviors[idx] == behavior

    def test_no_extra_behaviors(self):
        """Test nothing is appended past the expected behaviors."""
        assert len(self.fti.behaviors) == len(USER_PROFILE_BEHAVIORS)


class TestAffiliations:
    """A profile relates to Organizations without passing for a case study."""

    @pytest.fixture(autouse=True)
    def _setup(self, portal) -> Generator[None]:
        """Create an organization and a profile related to it; remove both after.

        The profile comes from the package's own API: UserProfile has an add
        permission no role holds, so ``api.content.create`` is refused even
        for a Manager.
        """
        self.portal = portal
        created: list[DexterityContent] = []
        try:
            with api.env.adopt_roles(["Manager"]):
                self.organization: DexterityContent = api.content.create(
                    container=portal, type="Organization", id="org", title="Org"
                )
                created.append(self.organization)
                self.profile: DexterityContent = profile_api.get_or_create(
                    "jdoe", "jdoe"
                )
                created.append(self.profile)
                api.relation.create(
                    source=self.profile,
                    target=self.organization,
                    relationship="affiliations",
                )
            yield
        finally:
            with api.env.adopt_roles(["Manager"]):
                api.content.delete(objects=created)

    def test_profile_provides_behavior(self):
        """Test the profile carries the affiliations field."""
        assert IAffiliations(self.profile, None) is not None

    def test_relation_is_stored_on_the_field(self):
        """Test the relation resolves forwards from the profile."""
        targets = [rel.to_object for rel in self.profile.affiliations]
        assert targets == [self.organization]

    def test_relation_is_found_backwards(self):
        """Test the organization finds the profile through ``affiliations``."""
        relations = api.relation.get(
            target=self.organization, relationship="affiliations"
        )
        assert [rel.from_object for rel in relations] == [self.profile]

    def test_profile_is_not_a_case_study(self):
        """Test the organization's case studies stay free of profiles."""
        case_studies = case_studies_for_organization(self.organization)
        assert case_studies == {"provided": [], "received": []}
