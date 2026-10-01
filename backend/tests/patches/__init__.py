"""Shared values for the runtime patch tests."""

#: Grid block columns whose ``image_scales`` the pinned plone.exportimport
#: 2.1.0 cannot handle. Each one raises a different exception upstream.
BROKEN_COLUMNS = {
    "missing": {"@id": "a"},
    "null": {"@id": "b", "image_scales": None},
    "empty-list": {"@id": "c", "image_scales": {"image": []}},
    "no-scales-key": {"@id": "d", "image_scales": {"image": [{"download": "old"}]}},
}

#: A column the upstream code already handled, kept as a control: the patch
#: must still rewrite its download urls.
HEALTHY_COLUMN = {
    "@id": "e",
    "image_scales": {
        "image": [{"download": "old", "scales": {"mini": {"download": "o"}}}]
    },
}


def grid_block(column: dict) -> dict:
    """Wrap a column in the smallest grid block ``parse_blocks`` accepts.

    :param column: the column payload to wrap.
    :returns: a blocks mapping with a single grid block.
    """
    return {"block-uid": {"@type": "grid", "columns": [{"image": [column]}]}}
