"""Atualização para 20261120001: atualiza o pas.plugins.identity à versão 1014."""

from . import PROFILE
from plonegovbr.site.upgrades.v20261120001 import IDENTITY_PROFILE
from Products.GenericSetup.tool import SetupTool

import pytest


SOURCE = "20261113001"
DESTINATION = "20261120001"

#: pas.plugins.identity:default profile version before 1.0.0a17.
IDENTITY_SOURCE = "1013"

#: Perfis que a versão 1.0.0a17 criou ao dividir o default. Um site instalado
#: antes dela não os tem registrados.
SPLIT_PROFILES = (
    "pas.plugins.identity:core",
    "pas.plugins.identity:contenttypes",
)


class TestUpgrade:
    """O passo de ``20261113001`` para ``20261120001``."""

    @pytest.fixture(autouse=True)
    def _setup(self, setup_tool: SetupTool) -> None:
        """Coloca o site e o pas.plugins.identity nas versões de origem.

        Os perfis divididos ficam sem versão registrada, como em um site
        instalado antes da versão 1014 do perfil.
        """
        self.setup_tool = setup_tool
        setup_tool.setLastVersionForProfile(PROFILE, SOURCE)
        setup_tool.setLastVersionForProfile(IDENTITY_PROFILE, IDENTITY_SOURCE)
        for profile in SPLIT_PROFILES:
            setup_tool.setLastVersionForProfile(profile, "unknown")

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

        assert [(s["ssource"], s["sdest"]) for s in steps] == [(SOURCE, DESTINATION)]

    def test_upgrades_identity(self):
        """Executá-lo leva o pas.plugins.identity à versão mais recente do perfil."""
        self._run()

        latest = self.setup_tool.getVersionForProfile(IDENTITY_PROFILE)
        assert self.setup_tool.getLastVersionForProfile(IDENTITY_PROFILE) == (latest,)
        assert self.setup_tool.listUpgrades(IDENTITY_PROFILE) == []

    @pytest.mark.parametrize("profile", SPLIT_PROFILES)
    def test_registers_split_profile(self, profile: str):
        """Executá-lo registra o perfil dividido como instalado.

        Sem o registro, o site continua com o perfil como não instalado.
        """
        assert self.setup_tool.getLastVersionForProfile(profile) == "unknown"

        self._run()

        assert self.setup_tool.getLastVersionForProfile(profile) != "unknown"
