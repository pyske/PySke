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

tests_has_critical = [test_has_critical_empty, test_has_critical_no, test_has_critical_yes]
	
# -------------------------- #

# TODO

tests_map_local = [] 

# -------------------------- #

# TODO

tests_reduce_local = [] 

# -------------------------- #

# TODO

tests_reduce_global = [] 

# -------------------------- #

# TODO

tests_uacc_local = [] 

# -------------------------- #

# TODO

tests_uacc_global = [] 

# -------------------------- #

# TODO

tests_uacc_update = [] 

# -------------------------- #

# TODO

tests_dacc_path = [] 

# -------------------------- #

# TODO

tests_dacc_global = [] 

# -------------------------- #

# TODO

tests_dacc_local = [] 

# -------------------------- #


fcts = tests_has_critical + tests_map_local \
	+ tests_reduce_local + tests_reduce_global \
	+ tests_uacc_local + tests_uacc_global + tests_uacc_update \
	+ tests_dacc_path + tests_dacc_global + tests_dacc_local

run_tests(fcts)
