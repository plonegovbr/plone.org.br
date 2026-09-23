"""Tests for the summary serializer metadata utility."""

from . import EXTRA_SUMMARY_FIELDS
from . import SUMMARY_DOCUMENT
from . import UTILITY_NAME
from plone.restapi.interfaces import IJSONSummarySerializerMetadata
from plone.restapi.interfaces import ISerializeToJsonSummary
from plonegovbr.site.serializers.summary import JSONSummarySerializerMetadata
from zope.component import getMultiAdapter
from zope.component import getUtility

import pytest


class TestSummarySerializerMetadata:
    """The utility declaring the extra metadata exposed on listings."""

    @pytest.fixture(autouse=True)
    def _setup(self, portal) -> None:
        """Look the utility up the way plone.restapi does."""
        self.portal = portal
        self.utility = getUtility(IJSONSummarySerializerMetadata, name=UTILITY_NAME)

    def test_utility_registered(self):
        """Test the ZCML registration resolves to our implementation."""
        assert isinstance(self.utility, JSONSummarySerializerMetadata)

    @pytest.mark.parametrize("field", sorted(EXTRA_SUMMARY_FIELDS))
    def test_declares_field(self, field: str):
        """Test a metadata field is declared."""
        assert field in self.utility.default_metadata_fields()

    def test_declares_nothing_else(self):
        """Every field costs a catalog lookup on every listing entry."""
        assert self.utility.default_metadata_fields() == set(EXTRA_SUMMARY_FIELDS)


@pytest.mark.portal(content=[SUMMARY_DOCUMENT], roles=["Manager"])
class TestSummarySerialization:
    """The declared metadata reaches the serialized summary."""

    @pytest.fixture(autouse=True)
    def _setup(self, portal, summary_document) -> None:
        """Serialize the provisioned Document the way a listing would.

        The site's own request is used on purpose: asking for the
        function-scoped ``http_request`` here would pull in a second layer.
        """
        self.portal = portal
        self.document = summary_document
        self.summary = getMultiAdapter(
            (self.document, self.portal.REQUEST), ISerializeToJsonSummary
        )()

    @pytest.mark.parametrize("field", sorted(EXTRA_SUMMARY_FIELDS))
    def test_field_in_summary(self, field: str):
        """Test a declared field is part of the serialized summary."""
        assert field in self.summary

    def test_subject_is_serialized(self):
        """Test the value, not only the key, survives serialization."""
        assert sorted(self.summary["Subject"]) == ["brasil", "plone"]
