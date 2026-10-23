"""Upgrade to 20261023001: run the collective.casestudy 2.0.0a4 upgrade steps."""

from plonegovbr.site import logger
from Products.GenericSetup.tool import SetupTool


#: Profile whose pending upgrade steps this version runs.
CASESTUDY_PROFILE = "collective.casestudy:default"


def upgrade_casestudy(setup_tool: SetupTool) -> None:
    """Run the pending upgrade steps of ``collective.casestudy:default``.

    In 2.0.0a4 that is the step to profile version 2600, which re-imports the
    package's own querystring fields so the Facet and Provider Services
    filters get their own translatable labels.

    :param setup_tool: The ``portal_setup`` tool.
    """
    before = setup_tool.getLastVersionForProfile(CASESTUDY_PROFILE)
    setup_tool.upgradeProfile(CASESTUDY_PROFILE)
    after = setup_tool.getLastVersionForProfile(CASESTUDY_PROFILE)
    logger.info(
        "Upgraded %s from %s to %s",
        CASESTUDY_PROFILE,
        ".".join(before),
        ".".join(after),
    )
