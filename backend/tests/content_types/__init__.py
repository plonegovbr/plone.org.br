"""Shared values for the content type tests."""

#: Behaviors enabled on the site root, in the order
#: ``profiles/default/types/Plone_Site.xml`` declares them. The order is part of
#: the contract: it drives the order of the fieldsets in the site controlpanel.
PLONE_SITE_BEHAVIORS = (
    "plonegovbr.socialmedia.settings",
    "sc.voltolighttheme.siteheader",
    "sc.voltolighttheme.themeselector",
    "sc.voltolighttheme.footer",
    "volto.preview_image_link",
    "plone.basic",
    "plone.relateditems",
    "plone.locking",
    "plone.excludefromnavigation",
    "volto.blocks",
)
