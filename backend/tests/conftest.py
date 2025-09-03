from plonegovbr.portal.testing import ACCEPTANCE_TESTING
from plonegovbr.portal.testing import FUNCTIONAL_TESTING
from plonegovbr.portal.testing import INTEGRATION_TESTING
from pytest_plone import fixtures_factory
from zope.component.hooks import site as site_wrapper

import pytest


pytest_plugins = ["pytest_plone"]


globals().update(
    fixtures_factory((
        (ACCEPTANCE_TESTING, "acceptance"),
        (FUNCTIONAL_TESTING, "functional"),
        (INTEGRATION_TESTING, "integration"),
    ))
)


@pytest.fixture(scope="class")
def portal_class(integration_class):
    if hasattr(integration_class, "testSetUp"):
        integration_class.testSetUp()
    portal = integration_class["portal"]
    with site_wrapper(portal):
        yield portal
    if hasattr(integration_class, "testTearDown"):
        integration_class.testTearDown()
