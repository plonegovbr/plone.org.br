"""Runtime patches applied to pinned dependencies.

These backport fixes that are already merged upstream but not yet released, so
every developer gets the same behaviour from a plain ``make install`` instead of
having to edit ``site-packages`` by hand.

Currently we patch ``plone.exportimport`` 2.1.0 with the two fixes merged in
`plone/plone.exportimport#111
<https://github.com/plone/plone.exportimport/pull/111>`_:

``_fix_image_paths`` (upstream issue #109)
    Grid block images exported without ``image_scales``, with a null value, with
    an empty scales list, or without a ``scales`` key raised ``TypeError``,
    ``IndexError`` or ``KeyError`` and broke both export and import.

The command line tools dropping protected fields (upstream issue #110)
    ``exporter_cli`` and ``importer_cli`` wrap their work in
    ``api.env.adopt_roles(["Manager"])``. Under ``adopt_roles`` a permission
    check only succeeds when the permission is granted to one of the adopted
    roles, which bypasses the unrestricted system user that ``get_app`` installs
    -- so the override can only *narrow* permissions. Fields whose read
    permission is granted to other roles were silently left out of the export.
    This is what emptied ``logo``, ``footer_logo`` and the whole footer
    configuration from the Plone Site root in the example content: the header
    settings behavior of ``sc.voltolighttheme`` grants its view permission to
    ``Anonymous`` and ``Authenticated``, not to ``Manager``.

Remove this module, and the ``apply_patches()`` call in
:mod:`plonegovbr.site`, once ``backend/pyproject.toml`` pins a
``plone.exportimport`` release that carries both fixes.
"""

from AccessControl.SecurityManagement import getSecurityManager
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import setSecurityManager
from AccessControl.users import system as system_user
from collections.abc import Callable
from collections.abc import Iterator
from contextlib import contextmanager
from functools import wraps
from plonegovbr.site import logger

import plone.exportimport.utils.content.blocks as exportimport_blocks
import sys


_applied = False


def _fix_image_paths(data: list) -> list[dict]:
    """Rewrite image urls to use the scale name.

    Replaces ``plone.exportimport.utils.content.blocks._fix_image_paths`` with
    the version merged upstream, which leaves untouched any entry that has no
    usable ``image_scales`` instead of raising.

    :param data: the image entries of a grid block column.
    :returns: the same entries, with the download urls rewritten.
    """
    parsed = []
    for info in data:
        image_scales = info.get("image_scales") or {}
        for field in image_scales:
            if not image_scales[field]:
                continue
            field_data = image_scales[field][0]
            field_data["download"] = f"@@images/{field}"
            for key, scale in field_data.get("scales", {}).items():
                scale["download"] = f"@@images/{field}/{key}"
        parsed.append(info)
    return parsed


@contextmanager
def _unrestricted() -> Iterator[None]:
    """Run the enclosed block as the unrestricted system user.

    This is the user ``plone.exportimport.utils.cli.get_app`` installs, and the
    one the command line tools are meant to run as. Entering this context
    undoes the narrowing that ``adopt_roles(["Manager"])`` performs around the
    export, and is a no-op once upstream drops that call.

    :returns: a context manager restoring the previous security manager on exit.
    """
    previous = getSecurityManager()
    newSecurityManager(None, system_user)
    try:
        yield
    finally:
        setSecurityManager(previous)


def _unrestrict(factory: Callable, method_name: str) -> Callable:
    """Wrap a ``get_exporter`` / ``get_importer`` factory.

    The returned factory produces the same object, with ``method_name`` bound to
    a version that runs inside :func:`_unrestricted`.

    :param factory: the original factory, taking the Plone Site.
    :param method_name: name of the method to wrap, on the object it returns.
    :returns: the wrapped factory.
    """

    @wraps(factory)
    def wrapped_factory(site):
        handler = factory(site)
        original = getattr(handler, method_name)

        @wraps(original)
        def runner(*args, **kwargs):
            with _unrestricted():
                return original(*args, **kwargs)

        setattr(handler, method_name, runner)
        return handler

    return wrapped_factory


def apply_patches() -> None:
    """Apply every patch in this module, once.

    Called from :mod:`plonegovbr.site`, which ZCML loads during Zope startup --
    and therefore from inside ``get_app()``, before the command line tools reach
    their ``adopt_roles`` block.
    """
    global _applied
    if _applied:
        return
    _applied = True

    exportimport_blocks._fix_image_paths = _fix_image_paths
    logger.info("Patched plone.exportimport blocks: _fix_image_paths (upstream #109)")

    # Only reachable when running under plone-exporter / plone-importer, which
    # is the only caller of these two names. Patching on a normal instance
    # start would import the command line helpers -- and Testing.makerequest
    # with them -- for no gain.
    cli = sys.modules.get("plone.exportimport.cli")
    if cli is None:
        return
    cli.get_exporter = _unrestrict(cli.get_exporter, "export_site")
    cli.get_importer = _unrestrict(cli.get_importer, "import_site")
    logger.info("Patched plone.exportimport cli: unrestricted export (upstream #110)")
