from pyske.ltree import VTag, parseVTag
from pyske.errors import UnknownTypeError 
from pyske.test.run import run_tests

def test_parseVTag_leaf():
	tag = "L"
	exp = VTag.LEAF
	res = parseVTag(tag)
	assert exp == res


def test_parseVTag_node():
	tag = "N"
	exp = VTag.NODE
	res = parseVTag(tag)
	assert exp == res


def test_parseVTag_critical():
	tag = "C"
	exp = VTag.CRITICAL
	res = parseVTag(tag)
	tag = "C"
	
	assert exp == res


def test_parseVTag_unknown():
	tag = "_"
	try:
		res = parseVTag(tag)
		raise Exception("Test failure")
	except UnknownTypeError as e:
		assert True


fcts = [test_parseVTag_leaf, test_parseVTag_node, test_parseVTag_critical, test_parseVTag_unknown]

run_tests(fcts)
