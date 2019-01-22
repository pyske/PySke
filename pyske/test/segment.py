from pyske.test.run import run_tests
from pyske.ltree import VTag, Segment, TaggedValue


def test_has_critical_empty():
	seg = Segment()
	exp = False
	res = seg.has_critical()
	assert exp == res


def test_has_critical_no():
	val1 = TaggedValue(1,"N")
	val2 = TaggedValue(2,"L")
	seg = Segment([val1, val2])
	exp = False
	res = seg.has_critical()
	assert exp == res


def test_has_critical_yes():
	val1 = TaggedValue(1,"N")
	val2 = TaggedValue(2,"L")
	val3 = TaggedValue(3,"C")
	seg = Segment([val1, val2, val3])
	exp = True
	res = seg.has_critical()
	assert exp == res
	
# -------------------------- #

# TODO

tests_map_local = [] 

# -------------------------- #

# -------------------------- #

# -------------------------- #


fcts = [test_has_critical_empty, test_has_critical_no, test_has_critical_yes]

run_tests(fcts)
