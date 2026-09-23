"""Shared values for the installation and profile tests."""

from plonegovbr.site import PACKAGE_NAME


DEFAULT_PROFILE = f"{PACKAGE_NAME}:default"
INITIAL_PROFILE = f"{PACKAGE_NAME}:initial"

#: Keep in sync with ``profiles/default/metadata.xml``.
DEFAULT_PROFILE_VERSION = "20260921001"

#: Profiles the default profile pulls in, directly or transitively.
#: ``collective.multiworkflow:default`` arrives through ``collective.casestudy``.
INSTALLED_PROFILES = (
    "Products.CMFEditions:CMFEditions",
    "Products.MimetypesRegistry:MimetypesRegistry",
    "Products.PlonePAS:PlonePAS",
    "Products.PortalTransforms:PortalTransforms",
    "collective.casestudy:default",
    "collective.multiworkflow:default",
    "pas.plugins.identity:default",
    "plone.app.contenttypes:default",
    "plone.app.linkintegrity:default",
    "plone.app.registry:default",
    "plone.app.theming:default",
    "plone.app.users:default",
    "plone.protect:default",
    "plone.restapi:blocks",
    "plone.restapi:default",
    "plone.staticresources:default",
    "plone.volto:default",
    "plonegovbr.site:default",
    "plonegovbr.socialmedia:default",
    "plonetheme.barceloneta:default",
    "sc.videos:default",
    "sc.voltolighttheme:default",
)

#: Profiles that must stay out of a fresh site.
#: ``kitconcept.voltolighttheme:default`` is the upstream of ``sc.voltolighttheme``
#: and installing both would register the theme twice; the ``:initial`` profiles
#: only exist to seed example content and are applied on demand.
NOT_INSTALLED_PROFILES = (
    "collective.casestudy:initial",
    "kitconcept.voltolighttheme:default",
    "pas.plugins.identity:initial",
    "plone.app.caching:default",
    "plone.app.discussion:default",
    "plone.app.iterate:default",
    "plone.app.multilingual:default",
    "plone.session:default",
    "plone.volto:initial",
    "plonegovbr.site:initial",
    "sc.videos:initial",
    "sc.voltolighttheme:initial",
)

#: ``(portal_type, title, klass)`` for every Dexterity type a fresh site has.
PORTAL_TYPES = (
    ("CaseStudy", "Case Study", "collective.casestudy.content.case_study.CaseStudy"),
    ("Collection", "Collection", "plone.app.contenttypes.content.Collection"),
    ("Document", "Page", "plone.volto.content.FolderishDocument"),
    ("Episode", "Episode", "sc.videos.content.episode.Episode"),
    ("Event", "Event", "plone.volto.content.FolderishEvent"),
    ("File", "File", "plone.app.contenttypes.content.File"),
    ("Folder", "Folder", "plone.app.contenttypes.content.Folder"),
    ("Image", "Image", "plone.app.contenttypes.content.Image"),
    ("Link", "Link", "plone.app.contenttypes.content.Link"),
    ("News Item", "News Item", "plone.volto.content.FolderishNewsItem"),
    (
        "Organization",
        "Organization",
        "collective.casestudy.content.organization.Organization",
    ),
    ("Plone Site", "Plone Site", "Products.CMFPlone.Portal.PloneSite"),
    (
        "PrincipalsContainer",
        "Principals folder",
        "pas.plugins.identity.core.contents.principals.PrincipalsContainer",
    ),
    ("UserGroup", "User Group", "pas.plugins.identity.core.contents.group.UserGroup"),
    (
        "UserProfile",
        "User Profile",
        "pas.plugins.identity.core.contents.profile.UserProfile",
    ),
    ("Video", "Video", "sc.videos.content.video.Video"),
    ("VideoSeries", "Series", "sc.videos.content.video_series.VideoSeries"),
)

#: Types the user can add anywhere in the site.
GLOBALLY_ALLOWED_TYPES = (
    "CaseStudy",
    "Document",
    "Episode",
    "Event",
    "File",
    "Image",
    "Link",
    "News Item",
    "Organization",
    "PrincipalsContainer",
    "UserGroup",
    "UserProfile",
    "Video",
    "VideoSeries",
)

#: Types registered in ``portal_repository``. An FTI carrying ``plone.versioning``
#: is not enough -- see the ``repositorytool.xml`` gotcha in the vault pattern.
VERSIONABLE_TYPES = (
    "CaseStudy",
    "Document",
    "Event",
    "Link",
    "News Item",
    "Organization",
    "UserGroup",
    "UserProfile",
    "Video",
)

#: Profiles hidden from the add-ons control panel by ``HiddenProfiles``.
#: Empty: the package ships only ``default`` and ``initial``, and hiding an
#: uninstall profile that does not exist is what this used to claim to do.
HIDDEN_PROFILES = ()

#: Products hidden from the add-ons control panel by ``HiddenProfiles``.
HIDDEN_PRODUCTS = (f"{PACKAGE_NAME}.upgrades",)
