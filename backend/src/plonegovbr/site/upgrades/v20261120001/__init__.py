"""Atualização para 20261120001: atualiza o pas.plugins.identity à versão 1014."""

from plonegovbr.site import logger
from Products.GenericSetup.tool import SetupTool


#: Perfil cujos passos de atualização pendentes esta versão executa.
IDENTITY_PROFILE = "pas.plugins.identity:default"


def upgrade_identity(setup_tool: SetupTool) -> None:
    """Executa os passos de atualização pendentes de ``pas.plugins.identity:default``.

    Na versão 1.0.0a17 o pendente é o passo para a versão 1014 do perfil. Esse
    passo registra ``pas.plugins.identity:core`` e
    ``pas.plugins.identity:contenttypes`` como instalados, sem importar nada,
    porque o perfil ``default`` passou a depender dos dois.

    :param setup_tool: A ferramenta ``portal_setup``.
    """
    before = setup_tool.getLastVersionForProfile(IDENTITY_PROFILE)
    setup_tool.upgradeProfile(IDENTITY_PROFILE)
    after = setup_tool.getLastVersionForProfile(IDENTITY_PROFILE)
    logger.info(
        "Upgraded %s from %s to %s",
        IDENTITY_PROFILE,
        ".".join(before),
        ".".join(after),
    )
