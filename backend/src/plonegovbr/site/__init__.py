"""Init and utils."""

from zope.i18nmessageid import MessageFactory

import logging


__version__ = "20260921.1"

PACKAGE_NAME = "plonegovbr.site"

_ = MessageFactory(PACKAGE_NAME)

logger = logging.getLogger(PACKAGE_NAME)

# Imported last: patches needs the logger defined above.
from plonegovbr.site.patches import apply_patches  # noqa: E402


apply_patches()
