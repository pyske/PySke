from pyske.test.run import run_tests
from pyske.errors import IllFormedError, NotEqualSizeError, ApplicationError
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

def test_uacc_local_empty():
	sum3 = lambda x,y,z : x + y + z
	id_f = lambda x : x
	seg = Segment()
	try:
		res = seg.uacc_local(sum3, id_f, sum3, sum3)
		raise Exception("Test failure")
	except IllFormedError as e:
		assert True


def test_uacc_local_illformed():
	sum3 = lambda x,y,z : x + y + z
	id_f = lambda x : x
	seg = Segment([TaggedValue(1,"N"), TaggedValue(2,"C")])
	try:
		res = seg.uacc_local(sum3, id_f, sum3, sum3)
		raise Exception("Test failure")
	except IllFormedError as e:
		assert True


def test_uacc_local_node():
	sum3 = lambda x,y,z : x + y + z
	id_f = lambda x : x
	seg = Segment([TaggedValue(1,"N"),  TaggedValue(2,"L"), TaggedValue(1,"N"), TaggedValue(2,"L"), TaggedValue(3,"C")])
	res = seg.uacc_local(sum3, id_f, sum3, sum3)
	exp = (9, Segment([TaggedValue(1,"N"),  TaggedValue(2,"L"), TaggedValue(1,"N"), TaggedValue(2,"L"), TaggedValue(3,"C")]))
	assert res == exp

def test_uacc_local_leaf():
	sum3 = lambda x,y,z : x + y + z
	id_f = lambda x : x
	seg = Segment([TaggedValue(1,"N"),  TaggedValue(2,"L"), TaggedValue(1,"N"), TaggedValue(2,"L"), TaggedValue(3,"L")])
	res = seg.uacc_local(sum3, id_f, sum3, sum3)
	exp = (9, Segment([TaggedValue(9,"N"),  TaggedValue(2,"L"), TaggedValue(6,"N"), TaggedValue(2,"L"), TaggedValue(3,"L")]))
	assert res == exp

tests_uacc_local = [test_uacc_local_empty, test_uacc_local_illformed, test_uacc_local_node, test_uacc_local_leaf] 

# -------------------------- #

def test_uacc_global_has_critical():
	sum3 = lambda x,y,z : x + y + z
	seg = Segment([TaggedValue(1,"N"), TaggedValue(2,"C"), TaggedValue(2,"L")])
	try:
		res = seg.uacc_global(sum3)
		raise Exception("Test failure")
	except IllFormedError as e:
		assert True


def test_uacc_global_empty():
	sum3 = lambda x,y,z : x + y + z
	seg = Segment()
	try:
		res = seg.uacc_global(sum3)
		raise Exception("Test failure")
	except IllFormedError as e:
		assert True


def test_uacc_global_illformed():
	sum3 = lambda x,y,z : x + y + z
	seg = Segment([TaggedValue(1,"N"), TaggedValue(2,"L")])
	try:
		res = seg.uacc_global(sum3)
		raise Exception("Test failure")
	except IllFormedError as e:
		assert True


def test_uacc_global_leaf():
	sum3 = lambda x,y,z : x + y + z
	id_f = lambda x : x
	seg = Segment([TaggedValue(3,"L")])
	res = seg.uacc_global(sum3)
	exp = Segment([TaggedValue(3,"L")])
	assert res == exp


def test_uacc_global_node():
	sum3 = lambda x,y,z : x + y + z
	id_f = lambda x : x
	seg = Segment([TaggedValue(1,"N"),  TaggedValue(2,"L"), TaggedValue(1,"N"), TaggedValue(2,"L"), TaggedValue(3,"L")])
	res = seg.uacc_global(sum3)
	exp = Segment([TaggedValue(9,"N"),  TaggedValue(2,"L"), TaggedValue(6,"N"), TaggedValue(2,"L"), TaggedValue(3,"L")])
	assert res == exp

tests_uacc_global = [test_uacc_global_has_critical, test_uacc_global_empty, test_uacc_global_illformed, test_uacc_global_leaf, test_uacc_global_node] 

# -------------------------- #

def test_uacc_update_empty():
	seg = Segment()
	sum3 = lambda x,y,z : x + y + z
	gt = Segment()
	lc = 1
	rc = 2
	try:
		res = seg.uacc_update(gt, sum3, lc, rc)
		raise Exception("Test failure")
	except IllFormedError as e:
		assert True


def test_uacc_update_not_same_size():
	seg = Segment([TaggedValue(1,"N"),  TaggedValue(2,"L"), TaggedValue(1,"N"), TaggedValue(2,"L"), TaggedValue(3,"L")])
	sum3 = lambda x,y,z : x + y + z
	gt = Segment()
	lc = 1
	rc = 2
	try:
		res = seg.uacc_update(gt, sum3, lc, rc)
		raise Exception("Test failure")
	except NotEqualSizeError as e:
		assert True


def test_uacc_update_illformed_node():
	seg = Segment([TaggedValue(1,"N"),  TaggedValue(2,"N"), TaggedValue(2,"N")])
	sum3 = lambda x,y,z : x + y + z
	gt = Segment([TaggedValue(1,"N"),  TaggedValue(2,"L"), TaggedValue(2,"L")])
	lc = 1
	rc = 2
	try:
		res = seg.uacc_update(gt, sum3, lc, rc)
		raise Exception("Test failure")
	except IllFormedError as e:
		assert True


def test_uacc_update_illformed_critical():
	seg = Segment([TaggedValue(1,"N"),  TaggedValue(2,"C"),TaggedValue(1,"N")])
	sum3 = lambda x,y,z : x + y + z
	gt = Segment([TaggedValue(1,"N"),  TaggedValue(2,"L"), TaggedValue(1,"L")])
	lc = 1
	rc = 2
	try:
		res = seg.uacc_update(gt, sum3, lc, rc)
		raise Exception("Test failure")
	except IllFormedError as e:
		assert True


def test_uacc_update_leaf():
	sum3 = lambda x,y,z : x + y + z
	seg = Segment([TaggedValue(1,"N"),  TaggedValue(2,"L"), TaggedValue(1,"N"), TaggedValue(2,"L"), TaggedValue(3,"L")])
	gt =  Segment([TaggedValue(9,"N"),  TaggedValue(2,"L"), TaggedValue(6,"N"), TaggedValue(2,"L"), TaggedValue(3,"L")])
	lc = 1
	rc = 2
	res = seg.uacc_update(gt, sum3, lc, rc)
	exp = Segment([TaggedValue(9,"N"),  TaggedValue(2,"L"), TaggedValue(6,"N"), TaggedValue(2,"L"), TaggedValue(3,"L")])
	assert res == exp


def test_uacc_update_node():
	sum3 = lambda x,y,z : x + y + z
	seg = Segment([TaggedValue(1,"N"),  TaggedValue(2,"L"), TaggedValue(1,"N"), TaggedValue(2,"L"), TaggedValue(3,"C")])
	gt = Segment([TaggedValue(1,"N"),  TaggedValue(2,"L"), TaggedValue(1,"N"), TaggedValue(2,"L"), TaggedValue(3,"C")])
	lc = 1
	rc = 2
	res = seg.uacc_update(gt, sum3, lc, rc)
	exp = Segment([TaggedValue(12,"N"),  TaggedValue(2,"L"), TaggedValue(9,"N"), TaggedValue(2,"L"), TaggedValue(6,"C")])
	assert res == exp

tests_uacc_update = [test_uacc_update_empty, test_uacc_update_not_same_size, test_uacc_update_illformed_node, test_uacc_update_illformed_critical, test_uacc_update_node, test_uacc_update_leaf] 

# -------------------------- #

def test_dacc_path_empty():
	seg = Segment()
	sum2 = lambda x,y : x + y
	id_f = lambda x : x
	try:
		res = seg.dacc_path(id_f, id_f, sum2)
		raise Exception("Test failure")
	except IllFormedError as e:
		assert True


def test_dacc_path_has_no_critical():
	seg = Segment([TaggedValue(1,"N"),TaggedValue(2,"L"),TaggedValue(3,"L")])
	sum2 = lambda x,y : x + y
	id_f = lambda x : x
	try:
		res = seg.dacc_path(id_f, id_f, sum2)
		raise Exception("Test failure")
	except ApplicationError as e:
		assert True


def test_dacc_path_gt_node():
	seg = Segment([TaggedValue(1,"N"),  TaggedValue(2,"L"), TaggedValue(1,"N"), TaggedValue(2,"L"), TaggedValue(3,"C")])
	sum2 = lambda x,y : x + y
	id_f = lambda x : x

	res = seg.dacc_path(id_f, id_f, sum2)
	exp = TaggedValue((5,5),"N")
	assert res == exp

tests_dacc_path = [test_dacc_path_empty, test_dacc_path_has_no_critical, test_dacc_path_gt_node] 

# -------------------------- #

def test_dacc_global_double_leaf():
	seg = Segment([TaggedValue(1,"L"), TaggedValue(1,"L")])
	sum2 = lambda x,y : x + y
	c = 2
	try:
		seg.dacc_global(sum2, c)
		raise Exception("Test failure")
	except IllFormedError as e :
		assert True


def test_dacc_global_has_critical():
	seg = Segment([TaggedValue(1,"N"), TaggedValue(1,"C"), TaggedValue(1,"L")])
	sum2 = lambda x,y : x + y
	c = 2
	try:
		seg.dacc_global(sum2, c)
		raise Exception("Test failure")
	except IllFormedError as e :
		assert True

def test_dacc_global():
	sum2 = lambda x,y : x + y
	c = 2
	seg = Segment([TaggedValue((1,1),"N"),  TaggedValue((2,3),"L"), TaggedValue((1,2),"N"), TaggedValue((2,2),"L"), TaggedValue((3,1),"L")])
	res = seg.dacc_global(sum2, c)
	exp = Segment([TaggedValue(2,"N"),  TaggedValue(3,"L"), TaggedValue(3,"N"), TaggedValue(4,"L"), TaggedValue(5,"L")])
	assert res == exp

tests_dacc_global = [test_dacc_global_double_leaf, test_dacc_global_has_critical, test_dacc_global] 

# -------------------------- #

def test_dacc_local_empty():
	seg = Segment()
	sum2 = lambda x, y: x + y
	c = 4
	try:
		seg.dacc_local(sum2, sum2, c)
		raise Exception("Test failure")
	except IllFormedError as e:
		assert True


def test_dacc_local_stack_empty_leaf():
	seg = Segment([TaggedValue(2,"L"),TaggedValue(2,"L")])
	sum2 = lambda x, y: x + y
	c = 4
	try:
		seg.dacc_local(sum2, sum2, c)
		raise Exception("Test failure")
	except IllFormedError as e:
		assert True


def test_dacc_local_stack_empty_critical():
	seg = Segment([TaggedValue(2,"C"),TaggedValue(2,"L")])
	sum2 = lambda x, y: x + y
	c = 4
	try:
		seg.dacc_local(sum2, sum2, c)
		raise Exception("Test failure")
	except IllFormedError as e:
		assert True


def test_dacc_local():
	seg = Segment([TaggedValue(231,"N"),  TaggedValue(169,"L"), TaggedValue(478,"N"), TaggedValue(634,"L"), TaggedValue(2,"C")])
	sum2 = lambda x, y: x + y
	min2 = lambda x, y: x - y
	c = 400
	res = seg.dacc_local(sum2, min2, c)
	exp = Segment([TaggedValue(400,"N"),  TaggedValue(631,"L"), TaggedValue(169,"N"), TaggedValue(647,"L"), TaggedValue(-309,"C")])
	assert res == exp

tests_dacc_local = [test_dacc_local_stack_empty_leaf, test_dacc_local_stack_empty_critical, test_dacc_local] 

# -------------------------- #


fcts = tests_has_critical + tests_map_local \
	+ tests_reduce_local + tests_reduce_global \
	+ tests_uacc_local + tests_uacc_global + tests_uacc_update \
	+ tests_dacc_path + tests_dacc_global + tests_dacc_local

run_tests(fcts, "segment")
