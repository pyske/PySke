from pyske.ltree import VTag, parseVTag
from pyske.errors import UnknownTypeError 

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
	assert exp == res


def test_parseVTag_unknown():
	tag = "_"
	try:
		res = parseVTag(tag)
		raise Exception("Test failure")
	except UnknownTypeError as e:
		assert True


fcts = [test_parseVTag_leaf, test_parseVTag_node, test_parseVTag_critical, test_parseVTag_unknown]

for f in fcts:
	try :
		f()
		print("\033[32m[OK] " +str(f) + "\033[0m")
	except Exception:
		print("\033[31m[KO] " +str(f)+ "\033[0m")

