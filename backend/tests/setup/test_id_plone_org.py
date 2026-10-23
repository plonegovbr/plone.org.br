"""Tests for the id.plone.org login provider set up by the default profile."""

from collections.abc import Generator
from plone import api
from plonegovbr.site.setuphandlers import configure_id_plone_org
from plonegovbr.site.setuphandlers import ID_PLONE_ORG_PREFIX
from plonegovbr.site.setuphandlers import ID_PLONE_ORG_SECRET_VARIABLE
from plonegovbr.site.setuphandlers import post_install

import pytest


class TestProviderRecords:
    """What the profile declares, before any secret is applied."""

    @pytest.fixture(autouse=True)
    def _setup(self, portal) -> None:
        """Bind the site to the instance."""
        self.portal = portal

    @pytest.mark.parametrize(
        "key,expected",
        [
            ("driver", "plone-identity"),
            ("title", "id.plone.org"),
            ("enabled", False),
            ("show_in_login", True),
            ("config.issuer", "https://id.plone.org"),
            ("config.client_id", "plone-org-br"),
            ("config.client_secret", None),
            ("config.userid_source", "username"),
            ("config.create_user", True),
            ("config.trust_email_verification", True),
            ("config.auto_link_by_email", True),
        ],
    )
    def test_record(self, key: str, expected):
        """Test a record of the id.plone.org provider."""
        value = api.portal.get_registry_record(f"{ID_PLONE_ORG_PREFIX}.{key}")
        assert value == expected

    def test_propertymap_extends_the_driver_default(self):
        """An empty map would fall back to the generic claims, not the driver's."""
        from pas.plugins.identity.core.drivers.identity import PloneIdentityDriver

        value = api.portal.get_registry_record(f"{ID_PLONE_ORG_PREFIX}.propertymap")
        expected = {**PloneIdentityDriver.default_propertymap}
        expected["social_links"] = "social_links"
        assert value == expected

    def test_propertymap_targets_are_mappable(self):
        """Every mapped field is one the package writes on a UserProfile."""
        from pas.plugins.identity.core.utils.propertymap import mappable_fields

        value = api.portal.get_registry_record(f"{ID_PLONE_ORG_PREFIX}.propertymap")
        fields = mappable_fields("UserProfile")
        assert sorted(set(value.values()) - set(fields)) == []

    def test_groupmap(self):
        """Test the id.plone.org editors group grants Site Administrators here."""
        value = api.portal.get_registry_record(f"{ID_PLONE_ORG_PREFIX}.groupmap")
        assert value == {"acl-plone-org-br-editors": "Site Administrators"}

    def test_groupmap_target_exists(self):
        """Test the local group the map grants is a group this site has."""
        assert api.group.get(groupname="Site Administrators") is not None

    def test_provider_is_listed(self):
        """The package reads the records back as a provider."""
        from pas.plugins.identity.api import provider

        config = provider.get("id-plone-org")
        assert config is not None
        assert config.driver_id == "plone-identity"


class TestConfigureIdPloneOrg:
    """The post handler applies the secret only when the environment has it."""

    @pytest.fixture(autouse=True)
    def _setup(self, portal) -> Generator[None]:
        """Bind the site and restore the records each test changes."""
        self.portal = portal
        names = (
            f"{ID_PLONE_ORG_PREFIX}.enabled",
            f"{ID_PLONE_ORG_PREFIX}.config.client_secret",
        )
        registry = api.portal.get_tool("portal_registry")
        saved = {name: registry[name] for name in names}
        yield
        # Not set_registry_record: plone.api refuses None, the secret's default.
        for name, value in saved.items():
            registry[name] = value

    def test_post_handler_is_registered(self):
        """Test the default profile runs the handler at the end of its import."""
        setup_tool = api.portal.get_tool("portal_setup")
        info = setup_tool.getProfileInfo("profile-plonegovbr.site:default")

        assert info["post_handler"] is post_install

    def test_without_secret(self, monkeypatch):
        """Test the provider stays disabled when the variable is not set."""
        monkeypatch.delenv(ID_PLONE_ORG_SECRET_VARIABLE, raising=False)

        assert configure_id_plone_org() is False
        assert api.portal.get_registry_record(f"{ID_PLONE_ORG_PREFIX}.enabled") is False

    def test_blank_secret(self, monkeypatch):
        """Test a variable holding only whitespace counts as not set."""
        monkeypatch.setenv(ID_PLONE_ORG_SECRET_VARIABLE, "   ")

        assert configure_id_plone_org() is False
        assert api.portal.get_registry_record(f"{ID_PLONE_ORG_PREFIX}.enabled") is False

    def test_with_secret(self, monkeypatch):
        """Test the secret is stored and the provider enabled."""
        monkeypatch.setenv(ID_PLONE_ORG_SECRET_VARIABLE, "not-a-real-secret")

        assert configure_id_plone_org() is True
        assert api.portal.get_registry_record(f"{ID_PLONE_ORG_PREFIX}.enabled") is True
        secret = api.portal.get_registry_record(
            f"{ID_PLONE_ORG_PREFIX}.config.client_secret"
        )
        assert secret == "not-a-real-secret"  # noqa: S105
