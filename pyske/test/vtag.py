from pyske.ltree import parseVTag,VTag_LEAF,VTag_NODE,VTag_CRITICAL
from pyske.errors import UnknownTypeError, TestFailure
from pyske.test.run import run_tests

def test_parseVTag_leaf():
	tag = "L"
	exp = VTag_LEAF
	res = parseVTag(tag)
	assert exp == res


def test_parseVTag_node():
	tag = "N"
	exp = VTag_NODE
	res = parseVTag(tag)
	assert exp == res


def test_parseVTag_critical():
	tag = "C"
	exp = VTag_CRITICAL
	res = parseVTag(tag)
	tag = "C"
	
	assert exp == res


def test_parseVTag_unknown():
	tag = "_"
	try:
		res = parseVTag(tag)
		raise TestFailure()
	except UnknownTypeError as e:
		assert True


fcts = [test_parseVTag_leaf, test_parseVTag_node, test_parseVTag_critical, test_parseVTag_unknown]

run_tests(fcts, "vtag")
