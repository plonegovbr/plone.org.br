from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing.zope import WSGI_SERVER_FIXTURE

import collective.volto.formsupport
import ploneorgbr.core


class PLONECONFCORELayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi

        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=collective.volto.formsupport)
        self.loadZCML(package=ploneorgbr.core)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "ploneorgbr.core:default")
        applyProfile(portal, "ploneorgbr.core:initial")


PLONECONF_CORE_FIXTURE = PLONECONFCORELayer()


PLONECONF_CORE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PLONECONF_CORE_FIXTURE,),
    name="PLONECONFCORELayer:IntegrationTesting",
)


PLONECONF_CORE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(PLONECONF_CORE_FIXTURE, WSGI_SERVER_FIXTURE),
    name="PLONECONFCORELayer:FunctionalTesting",
)


PLONECONF_COREACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        PLONECONF_CORE_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        WSGI_SERVER_FIXTURE,
    ),
    name="PLONECONFCORELayer:AcceptanceTesting",
)
