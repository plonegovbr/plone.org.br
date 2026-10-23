from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing.zope import WSGI_SERVER_FIXTURE

import collective.multiworkflow
import plonegovbr.site


class Layer(PloneSandboxLayer):
    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi

        self.loadZCML(package=plone.restapi)
        # collective.casestudy uses the plone:additionalworkflows directive,
        # declared in collective.multiworkflow's meta.zcml. A directive must be
        # defined before the file using it is parsed; a running site loads every
        # meta.zcml up front, a sandbox layer only what it is told to.
        self.loadZCML(name="meta.zcml", package=collective.multiworkflow)
        self.loadZCML(package=collective.multiworkflow)
        self.loadZCML(package=plonegovbr.site)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "plonegovbr.site:default")


FIXTURE = Layer()

INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name="Plonegovbr.SiteLayer:IntegrationTesting",
)


FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE, WSGI_SERVER_FIXTURE),
    name="Plonegovbr.SiteLayer:FunctionalTesting",
)


ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        WSGI_SERVER_FIXTURE,
    ),
    name="Plonegovbr.SiteLayer:AcceptanceTesting",
)
