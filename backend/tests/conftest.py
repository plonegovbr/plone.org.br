from plonegovbr.site.testing import ACCEPTANCE_TESTING
from plonegovbr.site.testing import FUNCTIONAL_TESTING
from plonegovbr.site.testing import INTEGRATION_TESTING
from pytest_plone import fixtures_factory

import os


# The default profile enables id.plone.org when this variable holds a secret,
# and `make test` exports backend/.env. Drop it before any layer is set up so
# the suite never sees, enables or prints a real secret; the tests that need
# the variable set it themselves with monkeypatch.
os.environ.pop("ID_PLONE_ORG_CLIENT_SECRET", None)

pytest_plugins = ["pytest_plone"]


globals().update(
    fixtures_factory((
        (ACCEPTANCE_TESTING, "acceptance"),
        (FUNCTIONAL_TESTING, "functional"),
        (INTEGRATION_TESTING, "integration"),
    ))
)
