"""Atualização para 20261113001: instala o plone.formblock no site."""

from . import PROFILE
from plonegovbr.site.upgrades.v20261113001 import FORMBLOCK_PROFILE
from Products.GenericSetup.tool import SetupTool

import pytest


SOURCE = "20261108001"
DESTINATION = "20261113001"

#: Versão do perfil plone.formblock:default em um site que não o tem.
FORMBLOCK_SOURCE = "unknown"


class TestUpgrade:
    """O passo de ``20261108001`` para ``20261113001``."""

    @pytest.fixture(autouse=True)
    def _setup(self, setup_tool: SetupTool) -> None:
        """Coloca o site na versão de origem, sem o plone.formblock registrado.

        A versão do perfil é apagada, como em um site instalado antes da
        dependência entrar no perfil padrão.
        """
        self.setup_tool = setup_tool
        setup_tool.setLastVersionForProfile(PROFILE, SOURCE)
        setup_tool.setLastVersionForProfile(FORMBLOCK_PROFILE, FORMBLOCK_SOURCE)

    def _steps(self) -> list[dict]:
        """Retorna os passos de atualização disponíveis a partir da versão de origem.

        ``listUpgrades`` devolve os passos de um grupo ``upgradeSteps`` como uma
        lista, e um ``upgradeStep`` isolado como uma única informação.
        """
        steps: list[dict] = []
        for entry in self.setup_tool.listUpgrades(PROFILE):
            steps.extend(entry if isinstance(entry, list) else [entry])
        return steps

    def _run(self) -> None:
        """Executa todos os passos disponíveis a partir da versão de origem."""
        for step in self._steps():
            step["step"].doStep(self.setup_tool)

    def test_available(self):
        """O site na versão de origem recebe exatamente este passo."""
        steps = self._steps()

        assert [(s["ssource"], s["sdest"]) for s in steps] == [
            (SOURCE, DESTINATION),
        ]

    def test_installs_formblock(self):
        """Executá-lo instala o plone.formblock na versão do perfil.

        Sem o registro da versão, o site continuaria com o perfil como não
        instalado, mesmo com o bloco disponível.
        """
        assert self.setup_tool.getLastVersionForProfile(FORMBLOCK_PROFILE) == (
            FORMBLOCK_SOURCE
        )

        self._run()

        expected = self.setup_tool.getVersionForProfile(FORMBLOCK_PROFILE)
        assert self.setup_tool.getLastVersionForProfile(FORMBLOCK_PROFILE) == (
            expected,
        )
