from kitconcept import api
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.restapi.testing import RelativeSession
from ploneorgbr.core.testing import PLONEORGBR_CORE_FUNCTIONAL_TESTING
from ploneorgbr.core.testing import PLONEORGBR_CORE_INTEGRATION_TESTING

import unittest


VOCABULARY = "ploneorgbr.vocabulary.industries"


class TestIndustriesVocabularyEndpoint(unittest.TestCase):

    layer = PLONEORGBR_CORE_FUNCTIONAL_TESTING

    endpoint = f"/@vocabularies/{VOCABULARY}"

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()

        self.api_session = RelativeSession(self.portal_url)
        self.api_session.headers.update({"Accept": "application/json"})

    def test_get_vocabulary_as_manager(self):
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        response = self.api_session.get(self.endpoint)
        self.assertEqual(200, response.status_code)
        response = response.json()
        self.assertEqual(len(response["items"]), 3)

    def test_get_vocabulary_as_anonymous(self):
        response = self.api_session.get(self.endpoint)
        self.assertEqual(200, response.status_code)
        response = response.json()
        self.assertEqual(len(response["items"]), 3)

    def test_get_vocabulary_translated(self):
        response = self.api_session.get(self.endpoint)
        self.assertEqual(200, response.status_code)
        response = response.json()
        self.assertEqual(len(response["items"]), 3)


class TestIndustriesVocabulary(unittest.TestCase):

    layer = PLONEORGBR_CORE_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()

    def test_vocabulary(self):
        vocab = api.vocabulary.get(VOCABULARY)

        items = [item.title for item in vocab]

        self.assertIn("Government", items)
