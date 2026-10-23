"""Who can call ``@video-metadata``, the service behind the video URL widget."""

from plone import api
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import TEST_USER_PASSWORD as PASSWORD
from Products.CMFPlone.Portal import PloneSite

import pytest
import transaction


USERNAME = "siteadmin"

#: A URL no provider resolves: the service answers 400 without going to the
#: network, which is enough to tell "allowed" apart from "unauthorized".
UNSUPPORTED_URL = "https://example.org/not-a-video"


class TestVideoMetadataPermission:
    """``@video-metadata`` is guarded by the Video add permission."""

    @pytest.fixture(autouse=True)
    def _setup(self, functional_portal: PloneSite, request_factory) -> None:
        """Create a Site Administrator and bind the request factory."""
        with api.env.adopt_user(username=SITE_OWNER_NAME):
            api.user.create(
                email="siteadmin@example.org",
                username=USERNAME,
                password=PASSWORD,
                roles=("Site Administrator",),
            )
        transaction.commit()
        self.request_factory = request_factory

    def _post(self, **kwargs) -> int:
        """POST an unsupported URL to the service and return the status code."""
        session = self.request_factory(**kwargs)
        response = session.post("/@video-metadata", json={"videoUrl": UNSUPPORTED_URL})
        return response.status_code

    def test_site_administrator(self):
        """A Site Administrator gets past the permission check."""
        assert self._post(basic_auth=(USERNAME, PASSWORD)) == 400

    def test_anonymous(self):
        """Anonymous is refused."""
        assert self._post() == 401
