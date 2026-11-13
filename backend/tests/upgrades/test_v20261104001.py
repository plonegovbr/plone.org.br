"""Upgrade to 20261104001: run the pas.plugins.identity 1.0.0a15 upgrade steps."""

from . import PROFILE
from plone import api
from plone.registry.interfaces import IRegistry
from plonegovbr.site.upgrades.v20261104001 import CLOUDFLARE_HEADERS
from plonegovbr.site.upgrades.v20261104001 import IDENTITY_PROFILE
from Products.GenericSetup.tool import SetupTool
from zope.component import getUtility

import pytest


SOURCE = "20261023001"
DESTINATION = "20261104001"

#: pas.plugins.identity:default profile version before 1.0.0a15.
IDENTITY_SOURCE = "1010"

#: The registry record upgrade step 1012 of pas.plugins.identity creates.
CLIENT_IP_HEADERS = "pas.plugins.identity.client_ip_headers"


class TestUpgrade:
    """The step from ``20261023001`` to ``20261104001``."""

    @pytest.fixture(autouse=True)
    def _setup(self, setup_tool: SetupTool) -> None:
        """Put the site and pas.plugins.identity back at their source versions.

        The client address record is removed, as a site upgraded from an
        earlier release does not have it.
        """
        self.setup_tool = setup_tool
        setup_tool.setLastVersionForProfile(PROFILE, SOURCE)
        setup_tool.setLastVersionForProfile(IDENTITY_PROFILE, IDENTITY_SOURCE)
        records = getUtility(IRegistry).records
        if CLIENT_IP_HEADERS in records:
            del records[CLIENT_IP_HEADERS]

    def _steps(self) -> list[dict]:
        """Return the upgrade steps available from the source version.

        ``listUpgrades`` gives the steps of an ``upgradeSteps`` group as one
        list, and a lone ``upgradeStep`` as a bare info.
        """
        steps: list[dict] = []
        for entry in self.setup_tool.listUpgrades(PROFILE):
            steps.extend(entry if isinstance(entry, list) else [entry])
        return steps

    def _run(self) -> None:
        """Run every step offered from the source version."""
        for step in self._steps():
            step["step"].doStep(self.setup_tool)

    def test_available(self):
        """The site at the source version is offered this step, then the next one.

        Steps chain: the step from 20261104001 is offered once the site is at
        its destination, so the list from the source carries both.
        """
        steps = self._steps()

        assert [(s["ssource"], s["sdest"]) for s in steps] == [
            (SOURCE, DESTINATION),
            (DESTINATION, "20261108001"),
            ("20261108001", "20261113001"),
        ]

    def test_upgrades_identity(self):
        """Running it brings pas.plugins.identity to its profile version."""
        self._run()

        expected = self.setup_tool.getVersionForProfile(IDENTITY_PROFILE)
        assert self.setup_tool.getLastVersionForProfile(IDENTITY_PROFILE) == (expected,)
        assert self.setup_tool.listUpgrades(IDENTITY_PROFILE) == []

    def test_creates_client_ip_headers(self):
        """The setting the 1.0.0a15 release reads is created on an upgraded site."""
        assert CLIENT_IP_HEADERS not in getUtility(IRegistry).records

        self._run()

        assert CLIENT_IP_HEADERS in getUtility(IRegistry).records

    def test_names_cloudflare_headers(self):
        """The site behind Cloudflare reads the visitor's address from them."""
        self._run()

        assert api.portal.get_registry_record(CLIENT_IP_HEADERS) == CLOUDFLARE_HEADERS
