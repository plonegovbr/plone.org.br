"""Init and utils."""

from zope.i18nmessageid import MessageFactory

import logging


__version__ = "20250903.1"

PACKAGE_NAME = "plonegovbr.portal"

_ = MessageFactory(PACKAGE_NAME)

logger = logging.getLogger(PACKAGE_NAME)
