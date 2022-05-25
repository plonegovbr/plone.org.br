from plone.indexer import indexer
from ploneorgbr.core.content.case_study import ICaseStudy


@indexer(ICaseStudy)
def industry_indexer(obj):
    return obj.industry
