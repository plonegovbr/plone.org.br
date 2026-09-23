"""Fixtures for the content type tests."""

from collections.abc import Generator
from Products.CMFPlone.Portal import PloneSite

import pytest


@pytest.fixture(scope="class")
def portal(portal_class) -> Generator[PloneSite]:
    """Yield the class-scoped Plone site.

    :param portal_class: Class-scoped Plone site, from ``pytest-plone``.
    :returns: Generator yielding the Plone site.
    """
    yield portal_class
