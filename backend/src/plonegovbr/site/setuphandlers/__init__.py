from plone import api
from plone.base.interfaces.installable import INonInstallable
from Products.GenericSetup.tool import SetupTool
from zope.interface import implementer

import logging
import os


logger = logging.getLogger("plonegovbr.site")

#: The provider the default profile declares for id.plone.org.
ID_PLONE_ORG_PREFIX = "pas.plugins.identity.providers.id-plone-org"

#: Environment variable holding the id.plone.org client secret.
ID_PLONE_ORG_SECRET_VARIABLE = "ID_PLONE_ORG_CLIENT_SECRET"  # noqa: S105 - a name


def configure_id_plone_org() -> bool:
    """Set the id.plone.org client secret and enable the provider.

    The secret never lives in the profile: it is read from
    :data:`ID_PLONE_ORG_SECRET_VARIABLE`. Without it the provider keeps the
    ``enabled = False`` the profile gives it, so a site with no secret shows
    no login button that could only fail.

    :returns: ``True`` when the secret was found and the provider enabled.
    """
    secret = os.environ.get(ID_PLONE_ORG_SECRET_VARIABLE, "").strip()
    if not secret:
        logger.info(
            "%s is not set; the id.plone.org provider stays disabled.",
            ID_PLONE_ORG_SECRET_VARIABLE,
        )
        return False
    api.portal.set_registry_record(
        f"{ID_PLONE_ORG_PREFIX}.config.client_secret", secret
    )
    api.portal.set_registry_record(f"{ID_PLONE_ORG_PREFIX}.enabled", True)
    logger.info("Enabled the id.plone.org provider.")
    return True


def post_install(context: SetupTool) -> None:
    """Finish the install once the ``default`` profile is imported.

    :param context: The setup tool running the import.
    """
    configure_id_plone_org()


@implementer(INonInstallable)
class HiddenProfiles:
    def getNonInstallableProfiles(self):
        """Hide no profile: this package ships no uninstall profile."""
        return []

    def getNonInstallableProducts(self):
        """Hide the upgrades package from site-creation and quickinstaller."""
        return [
            "plonegovbr.site.upgrades",
        ]
