"""Tests for the registry records written by the default profile."""

from . import CASE_STUDY_RECORDS
from . import SCALAR_RECORDS
from . import SEQUENCE_RECORDS
from . import THEME_COLORS
from plone import api

import pytest


class TestSiteSettings:
    """Site-wide settings a fresh site starts with."""

    @pytest.fixture(autouse=True)
    def _setup(self, portal) -> None:
        """Bind the site to the instance."""
        self.portal = portal

    @pytest.mark.parametrize("record,expected", SCALAR_RECORDS)
    def test_scalar_record(self, record: str, expected):
        """Test the value of a scalar registry record."""
        assert api.portal.get_registry_record(record) == expected

    @pytest.mark.parametrize("record,expected", SEQUENCE_RECORDS)
    def test_sequence_record(self, record: str, expected: list):
        """Test the value, and the order, of a sequence registry record."""
        assert list(api.portal.get_registry_record(record)) == expected


class TestThemeSettings:
    """The ``default`` theme definition of ``sc.voltolighttheme``."""

    prefix: str = "sc.voltolighttheme.theme.default"

    @pytest.fixture(autouse=True)
    def _setup(self, portal) -> None:
        """Bind the site to the instance."""
        self.portal = portal

    @pytest.mark.parametrize("key,expected", THEME_COLORS)
    def test_color(self, key: str, expected: str):
        """Test a color of the site theme."""
        assert api.portal.get_registry_record(f"{self.prefix}.{key}") == expected

    @pytest.mark.parametrize("key", ["font_family_primary", "font_family_secondary"])
    def test_font_family(self, key: str):
        """Test both font families point at the same typeface."""
        assert api.portal.get_registry_record(f"{self.prefix}.{key}") == (
            "Inter, sans-serif"
        )


class TestCaseStudySettings:
    """The vocabularies ``collective.casestudy`` reads from the registry."""

    @pytest.fixture(autouse=True)
    def _setup(self, portal) -> None:
        """Bind the site to the instance."""
        self.portal = portal

    @pytest.mark.parametrize("record,length,first_token", CASE_STUDY_RECORDS)
    def test_record(self, record: str, length: int, first_token: str):
        """Test the size and the leading term of a case study vocabulary."""
        terms = api.portal.get_registry_record(record)

        assert len(terms) == length
        assert terms[0]["token"] == first_token

    @pytest.mark.parametrize("record,length,first_token", CASE_STUDY_RECORDS)
    def test_record_terms_are_token_title_pairs(
        self, record: str, length: int, first_token: str
    ):
        """Every term is a ``{token, title}`` mapping.

        Before ``collective.casestudy`` profile version 2100 a term was the
        string ``"token|title"``; a site carrying the old shape would break the
        vocabulary rather than fail loudly.
        """
        terms = api.portal.get_registry_record(record)

        for term in terms:
            assert set(term) == {"token", "title"}
            assert term["token"]
            assert term["title"]

    def test_tokens_are_unique(self):
        """A duplicated token silently shadows a term in the vocabulary."""
        for record, _, _ in CASE_STUDY_RECORDS:
            terms = api.portal.get_registry_record(record)
            tokens = [term["token"] for term in terms]

            assert len(tokens) == len(set(tokens)), record
