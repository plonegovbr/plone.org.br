"""Atualização para 20261108001: executa os passos do pas.plugins.identity 1.0.0a16."""

from . import PROFILE
from plone import api
from plonegovbr.site.upgrades.v20261108001 import IDENTITY_PROFILE
from Products.GenericSetup.tool import SetupTool

import pytest


SOURCE = "20261104001"
DESTINATION = "20261108001"

#: pas.plugins.identity:default profile version before 1.0.0a16.
IDENTITY_SOURCE = "1012"

#: Ações de personal_tools que só o pas.plugins.identity declara.
IDENTITY_ACTIONS = ("identities", "identity_profile")


class TestUpgrade:
    """O passo de ``20261104001`` para ``20261108001``."""

    @pytest.fixture(autouse=True)
    def _setup(self, setup_tool: SetupTool) -> None:
        """Coloca o site e o pas.plugins.identity nas versões de origem.

        As ações do pas.plugins.identity são removidas, como em um site
        instalado antes da versão 1013 do perfil.
        """
        self.setup_tool = setup_tool
        self.portal = api.portal.get()
        setup_tool.setLastVersionForProfile(PROFILE, SOURCE)
        setup_tool.setLastVersionForProfile(IDENTITY_PROFILE, IDENTITY_SOURCE)
        actions = self.portal.portal_actions
        if "personal_tools" in actions.objectIds():
            category = actions.personal_tools
            for action_id in IDENTITY_ACTIONS:
                if action_id in category.objectIds():
                    category.manage_delObjects([action_id])

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

    def _action_ids(self) -> list[str]:
        """Retorna os ids das ações de personal_tools, ou uma lista vazia."""
        actions = self.portal.portal_actions
        if "personal_tools" not in actions.objectIds():
            return []
        return list(actions.personal_tools.objectIds())

    def test_available(self):
        """O site na versão de origem recebe este passo e o seguinte.

        Os passos se encadeiam: o passo de 20261108001 para 20261113001 é
        oferecido assim que o site chega ao destino, então a lista da origem
        traz os dois.
        """
        steps = self._steps()

        assert [(s["ssource"], s["sdest"]) for s in steps] == [
            (SOURCE, DESTINATION),
            (DESTINATION, "20261113001"),
        ]

    def test_upgrades_identity(self):
        """Executá-lo leva o pas.plugins.identity à versão 1013 do perfil."""
        self._run()

        assert self.setup_tool.getLastVersionForProfile(IDENTITY_PROFILE) == ("1013",)
        assert self.setup_tool.listUpgrades(IDENTITY_PROFILE) == []

    def test_adds_personal_tools_actions(self):
        """As ações do pas.plugins.identity passam a existir em personal_tools.

        Antes do passo elas não existem, e o menu do Volto 19.7 cai nas
        entradas padrão.
        """
        for action_id in IDENTITY_ACTIONS:
            assert action_id not in self._action_ids()

        self._run()

        assert set(IDENTITY_ACTIONS) <= set(self._action_ids())
