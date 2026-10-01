"""Tests for the runtime patches applied to plone.exportimport.

These exercise the upstream entry points, not our copies, so they fail if the
``apply_patches()`` call ever leaves :mod:`plonegovbr.site`.
"""

from . import BROKEN_COLUMNS
from . import grid_block
from . import HEALTHY_COLUMN
from plonegovbr.site import patches

import plone.exportimport.utils.content.blocks as exportimport_blocks
import pytest


class TestBlocksPatch:
    """Grid blocks without usable image_scales no longer break export."""

    def test_patch_is_wired(self):
        """Importing plonegovbr.site replaces the upstream implementation."""
        assert exportimport_blocks._fix_image_paths is patches._fix_image_paths

    @pytest.mark.parametrize("name", sorted(BROKEN_COLUMNS))
    def test_parse_blocks_survives(self, name: str):
        """Test a column the pinned release chokes on is left alone."""
        blocks = grid_block(BROKEN_COLUMNS[name])
        assert exportimport_blocks.parse_blocks(blocks) == blocks

    def test_parse_blocks_still_rewrites_urls(self):
        """Test the healthy case keeps working: downloads point at the scale."""
        parsed = exportimport_blocks.parse_blocks(grid_block(dict(HEALTHY_COLUMN)))
        image = parsed["block-uid"]["columns"][0]["image"][0]
        field_data = image["image_scales"]["image"][0]
        assert field_data["download"] == "@@images/image"
        assert field_data["scales"]["mini"]["download"] == "@@images/image/mini"


class TestUnrestrictedContext:
    """The export must run as the user get_app installs, never narrower."""

    @pytest.fixture(autouse=True)
    def _setup(self, security_manager) -> None:
        """Enter with a narrowed security manager, as adopt_roles leaves it."""
        from AccessControl.SecurityManagement import getSecurityManager
        from AccessControl.SecurityManagement import newSecurityManager
        from AccessControl.users import nobody

        newSecurityManager(None, nobody)
        self.narrowed = getSecurityManager()

    def test_installs_system_user(self):
        """Test the unrestricted system user is active inside the block."""
        from AccessControl.SecurityManagement import getSecurityManager
        from AccessControl.users import system

        with patches._unrestricted():
            assert getSecurityManager().getUser() is system

    def test_restores_previous_manager(self):
        """Test leaving the block puts the narrowed manager back."""
        from AccessControl.SecurityManagement import getSecurityManager

        with patches._unrestricted():
            pass
        assert getSecurityManager() is self.narrowed

    def test_restores_previous_manager_on_error(self):
        """Test the restore also happens when the body raises."""
        from AccessControl.SecurityManagement import getSecurityManager

        with pytest.raises(RuntimeError), patches._unrestricted():
            raise RuntimeError("boom")
        assert getSecurityManager() is self.narrowed


class TestUnrestrictFactory:
    """The wrapped get_exporter / get_importer factories."""

    @pytest.fixture(autouse=True)
    def _setup(self, security_manager) -> None:
        """Build a factory whose handler records the user it ran as."""
        from AccessControl.SecurityManagement import getSecurityManager
        from AccessControl.SecurityManagement import newSecurityManager
        from AccessControl.users import nobody

        self.seen = []
        outer = self

        class Handler:
            def export_site(self, path, options=None):
                outer.seen.append(getSecurityManager().getUser())
                return ["a result"]

        self.factory = patches._unrestrict(lambda site: Handler(), "export_site")
        newSecurityManager(None, nobody)

    def test_runs_as_system_user(self):
        """Test the wrapped method runs unrestricted."""
        from AccessControl.users import system

        self.factory(None).export_site("/some/path")
        assert self.seen == [system]

    def test_returns_the_original_result(self):
        """Test the wrapper is transparent to the caller."""
        assert self.factory(None).export_site("/some/path") == ["a result"]
