"""Shared values for the serializer tests."""

#: Name the ``IJSONSummarySerializerMetadata`` utility is registered under.
UTILITY_NAME = "plonegovbr.site.summary_serializer_metadata"

#: Catalog metadata this site adds to every listing, on top of what
#: ``plone.restapi`` returns by default.
EXTRA_SUMMARY_FIELDS = frozenset({
    "Subject",
    "effective",
    "image_field",
    "image_scales",
})

#: Content the ``portal`` marker provisions for the serialization test.
SUMMARY_DOCUMENT = {
    "type": "Document",
    "id": "summary-document",
    "title": "A Document",
    "subject": ("plone", "brasil"),
}
