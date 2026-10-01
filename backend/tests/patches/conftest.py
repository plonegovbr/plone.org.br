from collections.abc import Iterator

import pytest


@pytest.fixture()
def security_manager() -> Iterator[None]:
    """Restore the thread's security manager after a test swapped it."""
    from AccessControl.SecurityManagement import getSecurityManager
    from AccessControl.SecurityManagement import setSecurityManager

    previous = getSecurityManager()
    try:
        yield
    finally:
        setSecurityManager(previous)
