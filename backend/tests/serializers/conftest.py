"""Fixtures for the serializer tests."""

from . import SUMMARY_DOCUMENT
from collections.abc import Generator
from plone.dexterity.content import DexterityContent
from Products.CMFPlone.Portal import PloneSite

import pytest


@pytest.fixture(scope="class")
def portal(portal_class) -> Generator[PloneSite]:
    """Yield the class-scoped Plone site.

    :param portal_class: Class-scoped Plone site, from ``pytest-plone``.
    :returns: Generator yielding the Plone site.
    """
    yield portal_class


@pytest.fixture
def summary_document(portal) -> DexterityContent:
    """Return the Document the ``portal`` marker created.

    :param portal: Plone site.
    :returns: The Document to serialize.
    """
    return portal[SUMMARY_DOCUMENT["id"]]
