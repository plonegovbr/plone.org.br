"""Upgrade to 20261023001: run the collective.casestudy 2.0.0a4 upgrade steps."""

from . import PROFILE
from plone import api
from plonegovbr.site.upgrades.v20261023001 import CASESTUDY_PROFILE
from Products.GenericSetup.tool import SetupTool
from zope.i18nmessageid import Message

import pytest


SOURCE = "20260921001"
DESTINATION = "20261023001"

#: collective.casestudy profile version before 2.0.0a4.
CASESTUDY_SOURCE = "2500"

#: ``(registry record, msgid before 2600, msgid from 2600 on)``.
QUERYSTRING_LABELS = (
    (
        "plone.app.querystring.field.facets.title",
        "label_services",
        "label_facets",
    ),
    (
        "plone.app.querystring.field.services.title",
        "label_services",
        "label_provider_services",
    ),
)


class TestUpgrade:
    """The step from ``20260921001`` to ``20261023001``."""

    @pytest.fixture(autouse=True)
    def _setup(self, setup_tool: SetupTool) -> None:
        """Put the site and collective.casestudy back at their source versions.

        The querystring labels get the msgids they had before 2600.
        """
        self.setup_tool = setup_tool
        setup_tool.setLastVersionForProfile(PROFILE, SOURCE)
        setup_tool.setLastVersionForProfile(CASESTUDY_PROFILE, CASESTUDY_SOURCE)
        for name, old_msgid, _ in QUERYSTRING_LABELS:
            current = api.portal.get_registry_record(name)
            api.portal.set_registry_record(
                name,
                Message(old_msgid, domain=current.domain, default=current.default),
            )

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
        """The site at the source version is offered exactly this step."""
        steps = self._steps()

        assert [(s["ssource"], s["sdest"]) for s in steps] == [(SOURCE, DESTINATION)]

    def test_upgrades_casestudy(self):
        """Running it brings collective.casestudy to its profile version."""
        self._run()

        expected = self.setup_tool.getVersionForProfile(CASESTUDY_PROFILE)
        assert self.setup_tool.getLastVersionForProfile(CASESTUDY_PROFILE) == (
            expected,
        )
        assert self.setup_tool.listUpgrades(CASESTUDY_PROFILE) == []

    @pytest.mark.parametrize("name,_old,new_msgid", QUERYSTRING_LABELS)
    def test_fixes_the_label(self, name: str, _old: str, new_msgid: str):
        """The querystring filter gets its own translatable label."""
        self._run()

        assert api.portal.get_registry_record(name) == new_msgid

    def test_leaves_other_records_alone(self):
        """It runs collective.casestudy's steps, not a site-wide registry import."""
        api.portal.set_registry_record("plone.site_title", "Changed here")

        self._run()

        assert api.portal.get_registry_record("plone.site_title") == "Changed here"
