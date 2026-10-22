"""Tests for the UserProfile FTI and its relation to Organizations."""

from collections.abc import Generator
from collective.casestudy.utils.relations import case_studies_for_organization
from pas.plugins.identity.api import profile as profile_api
from plone import api
from plone.dexterity.content import DexterityContent
from plone.dexterity.fti import DexterityFTI
from plone.restapi.interfaces import ISerializeToJson
from plonegovbr.site.behaviors.affiliations import IAffiliations
from zope.component import getMultiAdapter

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

#: Fields an anonymous visitor reads on an active profile.
PUBLIC_FIELDS = ("fullname", "description", "home_page", "location")

#: Fields an anonymous visitor never reads.
PRIVATE_FIELDS = ("login", "group_ids", "email", "emails")


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


class TestUserProfileWorkflow:
    """Anonymous visitors see active profiles, never the protected fields."""

    @pytest.fixture(autouse=True)
    def _setup(self, portal) -> Generator[None]:
        """Create a profile for the tests; remove it after."""
        self.portal = portal
        self.profile: DexterityContent = profile_api.get_or_create("wfuser", "wfuser")
        yield
        with api.env.adopt_roles(["Manager"]):
            api.content.delete(obj=self.profile)

    def _anonymous_has(self, permission: str) -> bool:
        """Report whether Anonymous holds a permission on the profile."""
        with api.env.adopt_roles(["Anonymous"]):
            return bool(api.user.has_permission(permission, obj=self.profile))

    def _go_to(self, state: str) -> None:
        """Move the profile to a review state."""
        transitions = {"complete": "complete", "deactivated": "deactivate"}
        with api.env.adopt_roles(["Manager"]):
            api.content.transition(obj=self.profile, transition=transitions[state])
        assert api.content.get_state(obj=self.profile) == state

    def test_chain(self):
        """Test UserProfile uses this site's workflow."""
        chain = api.portal.get_tool("portal_workflow").getChainForPortalType(
            "UserProfile"
        )
        assert chain == ("plonegovbr_user_profile_workflow",)

    @pytest.mark.parametrize("state", ["incomplete", "complete"])
    @pytest.mark.parametrize(
        "permission",
        [
            "View",
            "Access contents information",
            "pas.plugins.identity: View Profile",
        ],
    )
    def test_anonymous_sees_active_profiles(self, state: str, permission: str):
        """Test Anonymous may open and read an incomplete or a complete profile."""
        if state != "incomplete":
            self._go_to(state)
        assert self._anonymous_has(permission) is True

    @pytest.mark.parametrize("state", ["incomplete", "complete"])
    @pytest.mark.parametrize(
        "permission",
        [
            "pas.plugins.identity: View Account Details",
            "pas.plugins.identity: View Personal Identifiable Information",
        ],
    )
    def test_anonymous_never_reads_protected_fields(self, state: str, permission: str):
        """Test Anonymous gets neither the login and groups nor email addresses.

        ``View Account Details`` guards ``login`` and ``group_ids``: granting
        it would show who is a Site Administrator.
        """
        if state != "incomplete":
            self._go_to(state)
        assert self._anonymous_has(permission) is False

    @pytest.mark.parametrize(
        "permission", ["View", "pas.plugins.identity: View Profile"]
    )
    def test_deactivated_profile_is_hidden(self, permission: str):
        """Test a deactivated profile stays out of anonymous reach."""
        self._go_to("deactivated")
        assert self._anonymous_has(permission) is False

    def test_anonymous_serialization(self):
        """Test the REST API shows Anonymous the public fields and nothing else."""
        with api.env.adopt_roles(["Manager"]):
            self.profile.fullname = "Workflow User"
            self.profile.description = "A description"
            self.profile.home_page = "https://example.org"
            self.profile.location = "Brasília"
        request = self.portal.REQUEST
        with api.env.adopt_roles(["Anonymous"]):
            data = getMultiAdapter((self.profile, request), ISerializeToJson)()
        public = {k: data.get(k) for k in PUBLIC_FIELDS}
        assert public == {
            "fullname": "Workflow User",
            "description": "A description",
            "home_page": "https://example.org",
            "location": "Brasília",
        }
        assert sorted(set(PRIVATE_FIELDS) & set(data)) == []


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
