"""Atualização para 20261113001: instala o plone.formblock no site."""

from plonegovbr.site import logger
from Products.GenericSetup.tool import SetupTool


#: Perfil que esta versão instala.
FORMBLOCK_PROFILE = "plone.formblock:default"


def install_formblock(setup_tool: SetupTool) -> None:
    """Instala ``plone.formblock:default`` em um site que já está no ar.

    Importa só esse perfil, e não todo o site, para não redefinir o que foi
    alterado no site desde a instalação. O prefixo ``profile-`` faz o
    GenericSetup registrar a versão do perfil ao final da importação.

    :param setup_tool: A ferramenta ``portal_setup``.
    """
    setup_tool.runAllImportStepsFromProfile(f"profile-{FORMBLOCK_PROFILE}")
    after = setup_tool.getLastVersionForProfile(FORMBLOCK_PROFILE)
    logger.info("Installed %s at version %s", FORMBLOCK_PROFILE, ".".join(after))
