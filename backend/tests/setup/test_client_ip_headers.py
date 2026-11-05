"""Tests for the client address headers the default profile sets for new sites."""

from plone import api
from plonegovbr.site.upgrades.v20261104001 import CLOUDFLARE_HEADERS

import pytest


CLIENT_IP_HEADERS = "pas.plugins.identity.client_ip_headers"


class TestClientIPHeaders:
    """The site sits behind Cloudflare, which names the visitor's address."""

    @pytest.fixture(autouse=True)
    def _setup(self, portal) -> None:
        """Bind the site to the instance."""
        self.portal = portal

    def test_names_cloudflare_headers(self):
        """A new site reads the visitor's address from the Cloudflare headers."""
        value = api.portal.get_registry_record(CLIENT_IP_HEADERS)

        assert value == CLOUDFLARE_HEADERS
