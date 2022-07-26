"""Upgrades tests for this package."""
from parameterized import parameterized
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from ploneorgbr.core.testing import PLONEORGBR_CORE_INTEGRATION_TESTING  # noqa: E501
from Products.GenericSetup.upgrade import listUpgradeSteps

import unittest


class UpgradeStepIntegrationTest(unittest.TestCase):

    layer = PLONEORGBR_CORE_INTEGRATION_TESTING
    profile = "ploneorgbr.core:default"

    def setUp(self):
        self.portal = self.layer["portal"]
        self.setup = self.portal["portal_setup"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def _match(self, item, source, dest):
        source, dest = tuple([source]), tuple([dest])
        return item["source"] == source and item["dest"] == dest

    def available_steps(self, src: str, dst: str) -> list:
        """Test available steps."""
        steps = listUpgradeSteps(self.setup, self.profile, src)
        steps = [s for s in steps if self._match(s[0], src, dst)]
        return steps

    @parameterized.expand(
        [
            ("20220523001", "20220525001", 1),
            ("20220525001", "20220712001", 1),
            ("20220712001", "20220726001", 1),
        ]
    )
    def test_available(self, src, dst, expected):
        """Test upgrade step is available."""
        steps = self.available_steps(src, dst)
        self.assertEqual(len(steps), expected)
