from kitconcept import api


def upgrade_plone(context):
    """Upgrade Plone to latest version."""
    mt = api.portal.get_tool("portal_migration")
    if mt.needUpgrading():
        mt.upgrade()
