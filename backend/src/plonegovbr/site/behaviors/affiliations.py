"""The organizations a person is affiliated with."""

from plone.app.vocabularies.catalog import StaticCatalogVocabulary
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from plonegovbr.site import _
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope.interface import provider


@provider(IFormFieldProvider)
class IAffiliations(model.Schema):
    """Relate a profile to one or more Organizations.

    Deliberately not ``collective.casestudy.organizations``: an Organization
    lists its case studies by looking up every ``organizations`` relation that
    points at it, whatever the source type, so profiles reusing that field
    would be listed as case studies. A field of its own keeps the two apart.
    """

    affiliations = RelationList(
        title=_("label_affiliations", default="Organizations"),
        description=_(
            "description_affiliations",
            default="Organizations this person works for or takes part in",
        ),
        required=False,
        default=[],
        value_type=RelationChoice(
            title=_("label_affiliation", default="Organization"),
            vocabulary=StaticCatalogVocabulary({
                "portal_type": ["Organization"],
            }),
        ),
    )
