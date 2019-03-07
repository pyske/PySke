import pytest

from pyske.core.tree.ltree import parse_tag,TAG_LEAF,TAG_NODE,TAG_CRITICAL
from pyske.core.support.errors import UnknownTypeError

def test_parseVTag_leaf():
	tag = "L"
	exp = TAG_LEAF
	res = parse_tag(tag)
	assert exp == res


def test_parseVTag_node():
	tag = "N"
	exp = TAG_NODE
	res = parse_tag(tag)
	assert exp == res


def test_parseVTag_critical():
	tag = "C"
	exp = TAG_CRITICAL
	res = parse_tag(tag)
	assert exp == res


def test_parseVTag_unknown():
	tag = "_"
	with pytest.raises(UnknownTypeError):
		parse_tag(tag)
