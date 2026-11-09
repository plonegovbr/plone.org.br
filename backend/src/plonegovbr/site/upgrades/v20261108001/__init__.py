"""Atualização para 20261108001: executa os passos do pas.plugins.identity 1.0.0a16."""

from plonegovbr.site import logger
from Products.GenericSetup.tool import SetupTool


#: Perfil cujos passos de atualização pendentes esta versão executa.
IDENTITY_PROFILE = "pas.plugins.identity:default"


def upgrade_identity(setup_tool: SetupTool) -> None:
    """Executa os passos de atualização pendentes de ``pas.plugins.identity:default``.

    Na versão 1.0.0a16 o pendente é o passo para a versão 1013 do perfil, que
    importa a categoria de ações ``personal_tools``. O menu de ferramentas
    pessoais do Volto 19.7 monta as entradas a partir dessa categoria, e um site
    instalado antes dela não a tem.

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
