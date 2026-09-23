"""Fixtures for the installation and profile tests."""

from collections.abc import Generator
from plone import api
from Products.CMFPlone.Portal import PloneSite

import pytest


@pytest.fixture(scope="class")
def portal(portal_class) -> Generator[PloneSite]:
    """Yield the class-scoped Plone site.

    Overriding ``portal`` keeps every fixture in this package on the same
    layer. Asking for the function-scoped ``portal`` alongside ``portal_class``
    instantiates two layers and two portals, and the teardown of the second one
    fails with ``TestIsolationBroken``.

    :param portal_class: Class-scoped Plone site, from ``pytest-plone``.
    :returns: Generator yielding the Plone site.
    """
    yield portal_class


@pytest.fixture
def versionable_content_types(portal) -> list[str]:
    """Return the portal types versioning is enabled for.

    :param portal: Plone site.
    :returns: Portal type ids registered in ``portal_repository``.
    """
    repo_tool = api.portal.get_tool("portal_repository")
    return repo_tool.getVersionableContentTypes()
