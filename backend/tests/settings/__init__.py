"""Shared values for the registry settings tests."""

#: Scalar registry records written by ``profiles/default/registry``.
SCALAR_RECORDS = (
    ("plone.site_title", "Plone Brasil"),
    ("plone.email_from_name", "Plone Brasil"),
    ("plone.default_language", "pt-br"),
    ("plone.sitemap_depth", 3),
    ("plone.sort_tabs_on", "getObjPositionInParent"),
    ("sc.videos.enable_series", True),
    ("sc.videos.youtube_api_enabled", False),
    ("sc.voltolighttheme.theme.default.name", "Plone Brasil"),
)

#: Sequence registry records, compared as lists to stay indifferent to whether
#: the registry hands back a list or a tuple.
SEQUENCE_RECORDS = (
    ("plone.available_languages", ["pt-br"]),
    ("plone.displayed_types", ["Link", "Document", "VideoSeries"]),
)

#: Colors of the ``default`` theme shipped by ``sc.voltolighttheme``, in the
#: Brazilian flag palette.
THEME_COLORS = (
    ("primary_color_light", "#ffffff"),
    ("primary_color_dark", "#000000"),
    ("primary_accent_color_light", "#0074a8"),
    ("secondary_color_light", "#002776"),
    ("secondary_accent_color_light", "#FFCC29"),
    ("accent_color_light", "#002776"),
)

#: ``collective.casestudy`` vocabulary records: ``(record, length, first token)``.
CASE_STUDY_RECORDS = (
    ("casestudy.versions", 17, "6.2"),
    ("casestudy.industries", 15, "edu"),
    ("casestudy.usages", 4, "portal"),
    ("casestudy.services", 4, "design"),
    ("casestudy.organization_sizes", 4, "me"),
)
