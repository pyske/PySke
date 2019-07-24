import pytest

from pyske.core.support.errors import UnknownTypeError
from pyske.core.tree.ltree import parse_tag, TAG_LEAF, TAG_NODE, TAG_CRITICAL


def test_parse_vtag_leaf():
    tag = "L"
    exp = TAG_LEAF
    res = parse_tag(tag)
    assert exp == res


def test_parse_vtag_node():
    tag = "N"
    exp = TAG_NODE
    res = parse_tag(tag)
    assert exp == res


def test_parse_vtag_critical():
    tag = "C"
    exp = TAG_CRITICAL
    res = parse_tag(tag)
    assert exp == res


def test_parse_vtag_unknown():
    tag = "_"
    with pytest.raises(UnknownTypeError):
        parse_tag(tag)
