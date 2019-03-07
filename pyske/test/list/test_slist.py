from pyske.core.support.errors import NotEqualSizeError, EmptyError
from pyske.core.list.slist import SList
import pytest

# -------------------------- #

def test_head_empty():
	sl = SList()
	exp = None
	res = sl.head()
	assert res == exp


def test_head_one():
	sl = SList()
	exp = 1
	sl.append(exp)
	res = sl.head()
	assert res == exp


def test_head_several():
	sl = SList()
	exp = 1
	sl.append(exp)
	sl.append(exp + 1)
	res = sl.head()
	assert res == exp


# -------------------------- #

def test_tail_empty():
	sl = SList()
	exp = SList()
	res = sl.tail()
	assert res == exp


def test_tail_one():
	sl = SList([1])
	exp = SList()
	res = sl.tail()
	assert res == exp


def test_tail_several():
	sl = SList([1, 2, 3])
	exp = SList([2, 3])
	res = sl.tail()
	assert res == exp


# -------------------------- #

def test_length_nil():
	sl = SList()
	exp = 0
	res = sl.length()
	assert res == exp


def test_length_cons():
	sl = SList([1, 2, 3])
	exp = 3
	res = sl.length()
	assert res == exp


# -------------------------- #

def test_filter():
	sl = SList([1, 2, 3, 4, 5, 6, 7, 8])
	p = lambda x : x%2 == 0
	res = sl.filter(p)
	for r in res:
		assert p(r)

# -------------------------- #

def test_empty_true():
	sl = SList()
	exp = True
	res = sl.is_empty()
	assert res == exp


def test_empty_false():
	sl = SList([1, 2, 3])
	exp = False
	res = sl.is_empty()
	assert res == exp

# -------------------------- #

def test_reverse_nil():
	sl = SList()
	exp = SList()
	res = sl.reverse()
	assert res == exp


def test_reverse_cons():
	sl = SList([1, 2, 3])
	exp = SList([3, 2, 1])
	res = sl.reverse()
	assert res == exp

# -------------------------- #

def test_map_empty():
	sl = SList()
	exp = SList()
	f = lambda x: x
	res = sl.map(f)
	assert res == exp


def test_map_inc():
	sl = SList([1, 2, 3])
	exp = SList([2, 3, 4])
	f = lambda x: x + 1
	res = sl.map(f)
	assert res == exp


def test_map_id():
	sl = SList([1, 2, 3])
	exp = SList([1, 2, 3])
	f = lambda x: x
	res = sl.map(f)
	assert res == exp

# -------------------------- #

def test_mapi_empty():
	sl = SList()
	exp = SList()
	f = lambda i, x: (i, x)
	res = sl.mapi(f)
	assert res == exp


def test_mapi_non_empty():
	sl = SList([1, 2, 3])
	exp = SList([0, 2, 6])
	f = lambda i, x: i * x
	res = sl.mapi(f)
	assert res == exp


def test_map_id():
	sl = SList([1, 2, 3])
	exp = SList([1, 2, 3])
	f = lambda i, x: x
	res = sl.mapi(f)
	assert res == exp

# -------------------------- #

def test_reduce_nil():
	e = 1232
	sl = SList()
	f = lambda x,y : x + y
	res = sl.reduce(f,e)
	exp = e
	assert res == exp

def test_reduce_cons():
	sl = SList([1, 2, 3, 4])
	f = lambda x,y : x + y
	res = sl.reduce(f)
	exp = 10
	assert res == exp

def test_reduce_sum_empty():
	sl = SList()
	f = lambda x,y : x + y
	exp = 0
	res = sl.reduce(f, 0)
	assert res == exp

def test_reduce_sum_non_empty():
	sl = SList([1,2,3,4,5,6])
	f = lambda x,y : x + y
	exp = 22
	res = sl.reduce(f, 1)
	assert res == exp

# -------------------------- #

def test_scan_nil():
	c = 0
	sl = SList()
	f = lambda x,y : x + y
	res = sl.scan(f, c)
	exp = SList([0])
	assert res == exp


def test_scan_cons():
	c = 0
	sl = SList([1, 2, 3, 4])
	f = lambda x,y : x + y
	res = sl.scan(f, c)
	exp = SList([0, 1, 3, 6, 10])
	assert res == exp

# -------------------------- #

def test_scanr_empty():
	with pytest.raises(AssertionError):
		sl = SList()
		f = lambda x, y: x + y
		sl.scanr(f)

def test_scanr_singleton():
	sl = SList([1])
	f = lambda x,y : x + y
	res = sl.scanr(f)
	assert res == sl


def test_scanr_non_singleton():
	sl = SList([1, 2, 3, 4])
	f = lambda x,y : x + y
	res = sl.scanr(f)
	exp = SList([1, 3, 6, 10])
	assert res == exp

# -------------------------- #

def test_scanl_empty():
	sl = SList([])
	f = lambda x,y : x + y
	res = sl.scanl(f,0)
	exp = SList([])
	assert res == exp


def test_scanl_non_empty():
	sl = SList([1, 2, 3, 4])
	f = lambda x,y : x + y
	res = sl.scanl(f, 0)
	exp = SList([0, 1, 3, 6])
	assert res == exp

# -------------------------- #

def test_scanl_last_empty():
	sl = SList([])
	f = lambda x,y : x + y
	res = sl.scanl_last(f, 0)
	exp = ([], 0)
	assert res == exp


def test_scanl_last_non_empty():
	sl = SList([1, 2, 3, 4])
	f = lambda x,y : x + y
	res = sl.scanl_last(f, 0)
	exp = ( SList([0, 1, 3, 6]), 10 )
	assert res == exp

# -------------------------- #

def test_rscan_nil():
	c = 0
	sl = SList()
	f = lambda x,y : x + y
	res = sl.scanp(f, c)
	exp = SList([0])
	assert res == exp


def test_rscan_cons():
	c = 0
	sl = SList([1, 2, 3, 4])
	f = lambda x,y : x + y
	res = sl.scanp(f, c)
	exp = SList([9, 7, 4, 0])
	assert res == exp

# -------------------------- #

def test_zip_nil():
	sl1 = SList()
	sl2 = SList()
	res = sl1.zip(sl2)
	exp = SList()
	assert res == exp


def test_zip_cons():
	sl1 = SList([1, 2, 3])
	sl2 = SList([2, 3, 4])
	res = sl1.zip(sl2)
	exp = SList([(1,2),(2,3),(3,4)])
	assert res == exp


def test_zip_one_gt():
	sl1 = SList([1, 2, 3])
	sl2 = SList([2, 3])
	try:
		res = sl1.zip(sl2)
		raise TestFailure()
	except NotEqualSizeError as e:
		assert True


def test_zip_one_lt():
	sl1 = SList([2, 3])
	sl2 = SList([2, 3, 4])
	try:
		res = sl1.zip(sl2)
		raise TestFailure()
	except NotEqualSizeError as e:
		assert True

# -------------------------- #

def test_zipwith_nil():
	sl1 = SList()
	sl2 = SList()
	f = lambda x,y : x + y
	res = sl1.zipwith(sl2, f)
	exp = SList()
	assert res == exp


def test_zipwith_cons():
	sl1 = SList([1, 2, 3])
	sl2 = SList([2, 3, 4])
	f = lambda x,y : x + y
	res = sl1.zipwith(sl2,f)
	exp = SList([3,5,7])
	assert res == exp


def test_zipwith_one_gt():
	sl1 = SList([1, 2, 3])
	sl2 = SList([2, 3])
	f = lambda x,y : x + y
	try:
		res = sl1.zipwith(sl2,f)
		raise TestFailure()
	except NotEqualSizeError as e:
		assert True


def test_zipwith_one_lt():
	sl1 = SList([2, 3])
	sl2 = SList([2, 3, 4])
	f = lambda x,y : x + y
	try:
		res = sl1.zipwith(sl2,f)
		raise TestFailure()
	except NotEqualSizeError as e:
		assert True

# -------------------------- #

def test_from_str_simple():
	s = "[1;2;3]"
	res = SList.from_str(s)
	exp = SList([1,2,3])
	assert res == exp


def parser_tuple(s):
	s = s.replace("(","")
	s = s.replace(")","")
	ss = s.split(",")
	return (int(ss[0]), int(ss[1]))


def test_from_str_tuple():
	s = "[(1,2);(3,4)]"
	res = SList.from_str(s, parser = parser_tuple)
	exp = SList([(1,2),(3,4)])
	assert res == exp

# -------------------------- #
