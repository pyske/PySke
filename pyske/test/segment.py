from pyske.test.run import run_tests
from pyske.errors import IllFormedError
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

def test_map_local():
	seg = Segment([TaggedValue(1,"N"), TaggedValue(2,"L"), TaggedValue(3,"C")])
	res = seg.map_local(lambda x : x + 1, lambda x : x - 1 )
	exp = Segment([TaggedValue(0,"N"), TaggedValue(3,"L"), TaggedValue(2,"C")])
	assert exp == res

tests_map_local = [test_map_local] 

# -------------------------- #

def test_reduce_local_empty():
	sum3 = lambda x,y,z : x + y + z
	id_f = lambda x : x
	seg = Segment()
	try:
		res = seg.reduce_local(sum3, id_f, sum3, sum3)
		raise Exception("Test failure")
	except IllFormedError as e:
		assert True


def test_reduce_local_illformed():
	sum3 = lambda x,y,z : x + y + z
	id_f = lambda x : x
	seg = Segment([TaggedValue(1,"N"), TaggedValue(2,"C")])
	try:
		res = seg.reduce_local(sum3, id_f, sum3, sum3)
		raise Exception("Test failure")
	except IllFormedError as e:
		assert True


def test_reduce_local_node():
	sum3 = lambda x,y,z : x + y + z
	id_f = lambda x : x
	seg = Segment([TaggedValue(1,"N"), TaggedValue(2,"L"), TaggedValue(3,"C")])	
	res = seg.reduce_local(sum3, id_f, sum3, sum3)
	exp = TaggedValue(6,"N")
	assert res == exp


def test_reduce_local_leaf():
	sum3 = lambda x,y,z : x + y + z
	id_f = lambda x : x
	seg = Segment([TaggedValue(1,"N"), TaggedValue(2,"L"), TaggedValue(3,"L")])	
	res = seg.reduce_local(sum3, id_f, sum3, sum3)
	exp = TaggedValue(6,"L")
	assert res == exp


tests_reduce_local = [test_reduce_local_empty, test_reduce_local_illformed, test_reduce_local_node, test_reduce_local_leaf] 

# -------------------------- #

def test_reduce_global_has_critical():
	sum3 = lambda x,y,z : x + y + z
	seg = Segment([TaggedValue(1,"N"), TaggedValue(2, "L"), TaggedValue(2,"C")])
	try:
		res = seg.reduce_global(sum3)
		raise Exception("Test failure")
	except IllFormedError as e:
		assert True


def test_reduce_global_empty():
	sum3 = lambda x,y,z : x + y + z
	seg = Segment()
	try:
		res = seg.reduce_global(sum3)
		raise Exception("Test failure")
	except IllFormedError as e:
		assert True


def test_reduce_global_illformed():
	sum3 = lambda x,y,z : x + y + z
	seg = Segment([TaggedValue(1,"N"), TaggedValue(2, "L")])
	try:
		res = seg.reduce_global(sum3)
		raise Exception("Test failure")
	except IllFormedError as e:
		assert True


def test_reduce_global_leaf():
	sum3 = lambda x,y,z : x + y + z
	seg = Segment([TaggedValue(2, "L")])
	res = seg.reduce_global(sum3)
	exp = 2
	assert res == exp


def test_reduce_global_node():
	sum3 = lambda x,y,z : x + y + z
	seg = Segment([TaggedValue(2, "N"),TaggedValue(2, "L"),TaggedValue(2, "L")])
	res = seg.reduce_global(sum3)
	exp = 6
	assert res == exp


tests_reduce_global = [test_reduce_global_has_critical,test_reduce_global_empty,test_reduce_global_illformed,test_reduce_global_leaf,test_reduce_global_node] 

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

run_tests(fcts, "segment")
