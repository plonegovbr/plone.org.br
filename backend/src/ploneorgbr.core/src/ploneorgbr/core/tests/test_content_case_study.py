from kitconcept import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from ploneorgbr.core.content.case_study import ICaseStudy
from ploneorgbr.core.testing import PLONEORGBR_CORE_INTEGRATION_TESTING
from zope.component import createObject

import unittest


class CaseStudyIntegrationTest(unittest.TestCase):

    layer = PLONEORGBR_CORE_INTEGRATION_TESTING

    portal_type = "CaseStudy"

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        fti = api.fti.get(self.portal_type)
        fti.global_allow = True

    def test_schema(self):
        fti = api.fti.get(self.portal_type)
        schema = fti.lookupSchema()
        self.assertEqual(ICaseStudy, schema)

    def test_fti(self):
        fti = api.fti.get(self.portal_type)
        self.assertTrue(fti)

    def test_factory(self):
        fti = api.fti.get(self.portal_type)
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(ICaseStudy.providedBy(obj))

    def test_adding(self):
        obj = api.content.create(
            container=self.portal,
            type=self.portal_type,
            title="Plone Foundation",
            industry="ngo",
            remoteUrl="https://plone.org/foundation",
        )
        self.assertTrue(ICaseStudy.providedBy(obj))
