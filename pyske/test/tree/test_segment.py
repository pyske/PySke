from pyske.core.support.errors import IllFormedError, NotEqualSizeError, ApplicationError, EmptyError, NotSameTagError
from pyske.core.tree.ltree import Segment, TaggedValue
import pytest

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

def test_map_local_empty():
	seg = Segment()
	res = seg.map_local(lambda x : x + 1, lambda x : x - 1 )
	exp = Segment()
	assert exp == res


def test_map_local():
	seg = Segment([TaggedValue(1,"N"), TaggedValue(2,"L"), TaggedValue(3,"C")])
	res = seg.map_local(lambda x : x + 1, lambda x : x - 1 )
	exp = Segment([TaggedValue(0,"N"), TaggedValue(3,"L"), TaggedValue(2,"C")])
	assert exp == res


# -------------------------- #

def test_reduce_local_empty():
	sum3 = lambda x,y,z : x + y + z
	id_f = lambda x : x
	seg = Segment()
	try:
		res = seg.reduce_local(sum3, id_f, sum3, sum3)
		raise TestFailure()
	except EmptyError as e:
		assert True


def test_reduce_local_illformed():
	sum3 = lambda x,y,z : x + y + z
	id_f = lambda x : x
	seg = Segment([TaggedValue(1,"N"), TaggedValue(2,"C")])
	try:
		res = seg.reduce_local(sum3, id_f, sum3, sum3)
		raise TestFailure()
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


# -------------------------- #

def test_reduce_global_has_critical():
	sum3 = lambda x,y,z : x + y + z
	seg = Segment([TaggedValue(1,"N"), TaggedValue(2, "L"), TaggedValue(2,"C")])
	try:
		res = seg.reduce_global(sum3)
		raise TestFailure()
	except ApplicationError as e:
		assert True


def test_reduce_global_empty():
	sum3 = lambda x,y,z : x + y + z
	seg = Segment()
	try:
		res = seg.reduce_global(sum3)
		raise TestFailure()
	except EmptyError as e:
		assert True


def test_reduce_global_illformed():
	sum3 = lambda x,y,z : x + y + z
	seg = Segment([TaggedValue(1,"N"), TaggedValue(2, "L")])
	try:
		res = seg.reduce_global(sum3)
		raise TestFailure()
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


# -------------------------- #

def test_uacc_local_empty():
	sum3 = lambda x,y,z : x + y + z
	id_f = lambda x : x
	seg = Segment()
	try :
		seg.uacc_local(sum3, id_f, sum3, sum3)
		raise TestFailure()
	except EmptyError as e:
		assert True


def test_uacc_local_illformed():
	sum3 = lambda x,y,z : x + y + z
	id_f = lambda x : x
	seg = Segment([TaggedValue(1,"N"), TaggedValue(2,"C")])
	try:
		res = seg.uacc_local(sum3, id_f, sum3, sum3)
		raise TestFailure()
	except IllFormedError as e:
		assert True


def test_uacc_local_node():
	sum3 = lambda x,y,z : x + y + z
	id_f = lambda x : x
	seg = Segment([TaggedValue(1,"N"),  TaggedValue(2,"L"), TaggedValue(1,"N"), TaggedValue(2,"L"), TaggedValue(3,"C")])
	res = seg.uacc_local(sum3, id_f, sum3, sum3)
	exp = (TaggedValue(9,"N"), Segment([None,  TaggedValue(2,"L"), None, TaggedValue(2,"L"), None]))
	assert res == exp

def test_uacc_local_leaf():
	sum3 = lambda x,y,z : x + y + z
	id_f = lambda x : x
	seg = Segment([TaggedValue(1,"N"),  TaggedValue(2,"L"), TaggedValue(1,"N"), TaggedValue(2,"L"), TaggedValue(3,"L")])
	res = seg.uacc_local(sum3, id_f, sum3, sum3)
	exp = (TaggedValue(9,"L"), Segment([TaggedValue(9,"N"),  TaggedValue(2,"L"), TaggedValue(6,"N"), TaggedValue(2,"L"), TaggedValue(3,"L")]))
	assert res == exp

# -------------------------- #
phi = lambda b : (1, 0, 0, 1)

def k(l, b, r):
	(ll, ls) = l
	(rl, rs) = r
	return (ls, ls + 1 + rs)


def psi_l(l, b, r):
	(l0, l1, l2, l3) = l
	(b0, b1, b2, b3) = b
	(rl, rs) = r
	res_0 = 0
	res_1 = b0 + b1
	res_2 = (b0 + b1) * l3 + b1 * (1 + rs) + b2
	res_3 = l3 + 1 + rs + b3
	return (res_0, res_1, res_2, res_3)


def psi_r(l, b, r):
	(ll, ls) = l
	(b0, b1, b2, b3) = b
	(r0, r1, r2, r3) = r
	res_0 = 0
	res_1 = b1
	res_2 = b1 * r3 + b0 * ls + b1 * (1 + ls) + b2
	res_3 = r3 + 1 + ls + b3
	return (res_0, res_1, res_2, res_3)


def psi_n(l, b, r):
	(ll, ls) = l
	(b0, b1, b2, b3) = b
	(rl, rs) = r
	res_1 = b0 * ls + b1 * (ls + rs + 1) + b2
	res_2 = ls + 1 + rs + b3
	return (res_1, res_2)


def test_uacc_local_prefix_1():
	seg = Segment([TaggedValue(1,"N"),  TaggedValue(2,"C"), TaggedValue((0,1),"L")])
	res = seg.uacc_local(k, phi, psi_l, psi_r)
	exp = (TaggedValue((0,1,1,4),"N"), Segment([None, None, TaggedValue((0,1),"L")]))
	assert res == exp


def test_uacc_local_prefix_2():
	seg = Segment([TaggedValue(4,"N"),  TaggedValue((0,1),"L"), TaggedValue((0,1),"L")])
	res = seg.uacc_local(k, phi, psi_l, psi_r)
	exp = (TaggedValue((1,3),"L"), Segment([TaggedValue((1,3),"N"), TaggedValue((0,1),"L"), TaggedValue((0,1),"L")]))
	assert res == exp


def test_uacc_local_prefix_3():
	seg = Segment([TaggedValue(5,"N"),  TaggedValue((0,1),"L"), TaggedValue((0,1),"L")])
	res = seg.uacc_local(k, phi, psi_l, psi_r)
	exp = (TaggedValue((1,3),"L"), Segment([TaggedValue((1,3),"N"), TaggedValue((0,1),"L"), TaggedValue((0,1),"L")]))
	assert res == exp


def test_uacc_global_prefix():
	gt = Segment([TaggedValue((0,1,1,4),"N"), TaggedValue((1,3),"L"),TaggedValue((1,3),"L")])
	res = gt.uacc_global(psi_n)
	exp = Segment([TaggedValue((8,11),"N"), TaggedValue((1,3),"L"),TaggedValue((1,3),"L")])
	assert res == exp


def test_uacc_update_prefix():
	seg = Segment([TaggedValue(1,"N"),TaggedValue(2,"C"),TaggedValue((0,1),"L")])
	seg2 = Segment([None, None ,TaggedValue((0,1),"L")])
	lc = (1,3)
	rc = (1,3)
	res = seg.uacc_update(seg2, k, lc, rc)
	exp = Segment([TaggedValue((5,9),"N"),TaggedValue((1,5),"C"),TaggedValue((0,1),"L")])
	assert res == exp


# -------------------------- #

def test_uacc_global_has_critical():
	sum3 = lambda x,y,z : x + y + z
	seg = Segment([TaggedValue(1,"N"), TaggedValue(2,"C"), TaggedValue(2,"L")])
	try:
		res = seg.uacc_global(sum3)
		raise TestFailure()
	except ApplicationError as e:
		assert True


def test_uacc_global_empty():
	sum3 = lambda x,y,z : x + y + z
	seg = Segment()
	exp = Segment()
	res = seg.uacc_global(sum3)
	assert exp == res


def test_uacc_global_illformed():
	sum3 = lambda x,y,z : x + y + z
	seg = Segment([TaggedValue(1,"N"), TaggedValue(2,"L")])
	try:
		res = seg.uacc_global(sum3)
		raise TestFailure()
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

# -------------------------- #

def test_uacc_update_empty():
	seg = Segment()
	sum3 = lambda x,y,z : x + y + z
	gt = Segment()
	lc = 1
	rc = 2
	res = seg.uacc_update(gt, sum3, lc, rc)
	exp = Segment()
	assert res == exp


def test_uacc_update_not_same_size():
	seg = Segment([TaggedValue(1,"N"),  TaggedValue(2,"L"), TaggedValue(1,"N"), TaggedValue(2,"L"), TaggedValue(3,"L")])
	sum3 = lambda x,y,z : x + y + z
	gt = Segment()
	lc = 1
	rc = 2
	try:
		res = seg.uacc_update(gt, sum3, lc, rc)
		raise TestFailure()
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
		raise TestFailure()
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
		raise TestFailure()
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

# -------------------------- #

def test_dacc_path_empty():
	seg = Segment()
	sum2 = lambda x,y : x + y
	id_f = lambda x : x
	try:
		res = seg.dacc_path(id_f, id_f, sum2)
		raise TestFailure()
	except EmptyError as e:
		assert True


def test_dacc_path_has_no_critical():
	seg = Segment([TaggedValue(1,"N"),TaggedValue(2,"L"),TaggedValue(3,"L")])
	sum2 = lambda x,y : x + y
	id_f = lambda x : x
	try:
		res = seg.dacc_path(id_f, id_f, sum2)
		raise TestFailure()
	except ApplicationError as e:
		assert True


def test_dacc_path_gt_node():
	seg = Segment([TaggedValue(1,"N"),  TaggedValue(2,"L"), TaggedValue(1,"N"), TaggedValue(2,"L"), TaggedValue(3,"C")])
	sum2 = lambda x,y : x + y
	id_f = lambda x : x

	res = seg.dacc_path(id_f, id_f, sum2)
	exp = TaggedValue((5,5),"N")
	assert res == exp

# -------------------------- #

def test_dacc_global_double_leaf():
	seg = Segment([TaggedValue(1,"L"), TaggedValue(1,"L")])
	sum2 = lambda x,y : x + y
	c = 2
	try:
		seg.dacc_global(sum2, c)
		raise TestFailure()
	except IllFormedError as e :
		assert True


def test_dacc_global_empty():
	seg = Segment()
	sum2 = lambda x,y : x + y
	c = 2
	res = seg.dacc_global(sum2, c)
	exp = Segment()
	assert res == exp


def test_dacc_global_has_critical():
	seg = Segment([TaggedValue(1,"N"), TaggedValue(1,"C"), TaggedValue(1,"L")])
	sum2 = lambda x,y : x + y
	c = 2
	try:
		seg.dacc_global(sum2, c)
		raise TestFailure()
	except ApplicationError as e :
		assert True

def test_dacc_global():
	sum2 = lambda x,y : x + y
	c = 2
	seg = Segment([TaggedValue((1,1),"N"),  TaggedValue((2,3),"L"), TaggedValue((1,2),"N"), TaggedValue((2,2),"L"), TaggedValue((3,1),"L")])
	res = seg.dacc_global(sum2, c)
	exp = Segment([TaggedValue(2,"N"),  TaggedValue(3,"L"), TaggedValue(3,"N"), TaggedValue(4,"L"), TaggedValue(5,"L")])
	assert res == exp

# -------------------------- #

def test_dacc_local_empty():
	seg = Segment()
	sum2 = lambda x, y: x + y
	c = 4
	res = seg.dacc_local(sum2, sum2, c)
	exp = Segment()
	assert res == exp


def test_dacc_local_stack_empty_leaf():
	seg = Segment([TaggedValue(2,"L"),TaggedValue(2,"L")])
	sum2 = lambda x, y: x + y
	c = 4
	try:
		seg.dacc_local(sum2, sum2, c)
		raise TestFailure()
	except IllFormedError as e:
		assert True


def test_dacc_local_stack_empty_critical():
	seg = Segment([TaggedValue(2,"C"),TaggedValue(2,"L")])
	sum2 = lambda x, y: x + y
	c = 4
	try:
		seg.dacc_local(sum2, sum2, c)
		raise TestFailure()
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

# -------------------------- #

def test_get_left_has_critical():
	gt = Segment([TaggedValue(2,"N"),TaggedValue(1,"C"),TaggedValue(2,"L")])
	i = 0
	try:
		gt.get_left(i)
		raise TestFailure()
	except ApplicationError as e:
		assert True


def test_get_left_is_leaf():
	gt = Segment([TaggedValue(2,"N"),TaggedValue(1,"L"),TaggedValue(2,"L")])
	i = 1
	try:
		gt.get_left(i)
		raise TestFailure()
	except ApplicationError as e:
		assert True


def test_get_left_illformed():
	gt = Segment([TaggedValue(2,"N")])
	i = 0
	try:
		gt.get_left(i)
		raise TestFailure()
	except IllFormedError as e:
		assert True


def test_get_left():
	gt = Segment([TaggedValue(2,"N"),TaggedValue(1,"L"),TaggedValue(2,"L")])
	i = 0
	res = gt.get_left(i)
	exp = TaggedValue(1,"L")
	assert res == exp


# -------------------------- #

def test_get_right_has_critical():
	gt = Segment([TaggedValue(2,"N"),TaggedValue(1,"C"),TaggedValue(2,"L")])
	i = 0
	try:
		gt.get_right(i)
		raise TestFailure()
	except ApplicationError as e:
		assert True


def test_get_right_is_leaf():
	gt = Segment([TaggedValue(2,"N"),TaggedValue(1,"L"),TaggedValue(2,"L")])
	i = 1
	try:
		gt.get_right(i)
		raise TestFailure()
	except ApplicationError as e:
		assert True


def test_get_right_illformed():
	gt = Segment([TaggedValue(2,"N"),TaggedValue(1,"L")])
	i = 0
	try:
		gt.get_right(i)
		raise TestFailure()
	except IllFormedError as e:
		assert True


def test_get_right_direct():
	gt = Segment([TaggedValue(2,"N"),TaggedValue(1,"L"),TaggedValue(2,"L")])
	i = 0
	res = gt.get_right(i)
	exp = TaggedValue(2,"L")
	assert res == exp


def test_get_right_not_direct():
	gt = Segment([TaggedValue(1,"N"),TaggedValue(3,"N"),TaggedValue(8,"L"),TaggedValue(4,"L"),TaggedValue(2,"L")])
	i = 0
	res = gt.get_right(i)
	exp = TaggedValue(2,"L")
	assert res == exp


# -------------------------- #

def test_zip_not_equal_size_error():
	seg1 = Segment([TaggedValue(2,"N"),TaggedValue(1,"L"),TaggedValue(2,"L")])
	seg2 = Segment([TaggedValue(2,"L")])
	try :
		seg1.zip(seg2)
		raise TestFailure()
	except NotEqualSizeError :
		assert True


def test_zip_not_same_tag_error():
	seg1 = Segment([TaggedValue(2,"N"),TaggedValue(1,"L"),TaggedValue(2,"L")])
	seg2 = Segment([TaggedValue(2,"N"),TaggedValue(1,"C"),TaggedValue(2,"L")])
	try :
		seg1.zip(seg2)
		raise TestFailure()
	except NotSameTagError:
		assert True


def test_zip():
	seg1 = Segment([TaggedValue(1,"N"),TaggedValue(2,"L"),TaggedValue(3,"L")])
	seg2 = Segment([TaggedValue(4,"N"),TaggedValue(5,"L"),TaggedValue(6,"L")])
	res = seg1.zip(seg2)
	exp = Segment([TaggedValue((1,4),"N"),TaggedValue((2,5),"L"),TaggedValue((3,6),"L")])
	assert res == exp

# -------------------------- #


def test_zipwith_not_equal_size_error():
	sum2 = lambda x,y : x + y
	seg1 = Segment([TaggedValue(2,"N"),TaggedValue(1,"L"),TaggedValue(2,"L")])
	seg2 = Segment([TaggedValue(2,"L")])
	with pytest.raises(NotEqualSizeError):
		seg1.map2(sum2, seg2)


def test_zipwith_not_same_tag_error():
	sum2 = lambda x,y : x + y
	seg1 = Segment([TaggedValue(2,"N"),TaggedValue(1,"L"),TaggedValue(2,"L")])
	seg2 = Segment([TaggedValue(2,"N"),TaggedValue(1,"C"),TaggedValue(2,"L")])
	with pytest.raises(NotSameTagError):
		seg1.map2(sum2, seg2)


def test_zipwith():
	sum2 = lambda x,y : x + y
	seg1 = Segment([TaggedValue(1,"N"),TaggedValue(2,"L"),TaggedValue(3,"L")])
	seg2 = Segment([TaggedValue(4,"N"),TaggedValue(5,"L"),TaggedValue(6,"L")])
	res = seg1.map2(sum2, seg2)
	exp = Segment([TaggedValue(5,"N"),TaggedValue(7,"L"),TaggedValue(9,"L")])
	assert res == exp

# -------------------------- #

def test_from_str():
	s = "[(11^N); (2^L); (3^C)]"
	res = Segment.from_str(s)
	exp = Segment([TaggedValue(11,"N"),TaggedValue(2,"L"),TaggedValue(3,"C")])
	assert res == exp

# -------------------------- #