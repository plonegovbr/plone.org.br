"""Upgrade to 20261104001: run the pas.plugins.identity 1.0.0a15 upgrade steps."""

from plone import api
from plonegovbr.site import logger
from Products.GenericSetup.tool import SetupTool


#: Profile whose pending upgrade steps this version runs.
IDENTITY_PROFILE = "pas.plugins.identity:default"

#: The registry record naming the headers that carry the visitor's address.
CLIENT_IP_HEADERS = "pas.plugins.identity.client_ip_headers"

#: The site sits behind Cloudflare, which sets these to the visitor's address.
CLOUDFLARE_HEADERS = ("CF-Connecting-IPv6", "CF-Connecting-IP")


def upgrade_identity(setup_tool: SetupTool) -> None:
    """Run the pending upgrade steps of ``pas.plugins.identity:default``.

    In 1.0.0a15 those are the steps to profile version 1011, which map the
    View Account Details permission onto every profile in the site, and to
    1012, which creates the ``client_ip_headers`` setting, empty. Then the
    setting names the Cloudflare headers, as the default profile does for
    new sites.

    :param setup_tool: The ``portal_setup`` tool.
    """
    before = setup_tool.getLastVersionForProfile(IDENTITY_PROFILE)
    setup_tool.upgradeProfile(IDENTITY_PROFILE)
    after = setup_tool.getLastVersionForProfile(IDENTITY_PROFILE)
    api.portal.set_registry_record(CLIENT_IP_HEADERS, CLOUDFLARE_HEADERS)
    logger.info(
        "Upgraded %s from %s to %s",
        IDENTITY_PROFILE,
        ".".join(before),
        ".".join(after),
    )
