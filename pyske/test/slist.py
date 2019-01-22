from pyske.errors import NotEqualSizeError, EmptyError
from pyske.slist import SList

# -------------------------- #

def test_head_1():
	sl = SList()
	exp = None
	res = sl.head()
	assert res == exp


def test_head_2():
	sl = SList()
	exp = 1
	sl.append(exp)
	res = sl.head()
	assert res == exp


def test_head_3():
	sl = SList()
	exp = 1
	sl.append(exp)
	sl.append(exp + 1)
	res = sl.head()
	assert res == exp


tests_head = [test_head_1, test_head_2, test_head_3]

# -------------------------- #

def test_tail_1():
	sl = SList()
	exp = SList()
	res = sl.tail()
	assert res == exp


def test_tail_2():
	sl = SList([1])
	exp = SList()
	res = sl.tail()
	assert res == exp


def test_tail_3():
	sl = SList([1, 2, 3])
	exp = SList([2, 3])
	res = sl.tail()
	assert res == exp


tests_tail = [test_tail_1, test_tail_2, test_tail_3]

# -------------------------- #

def test_length_1():
	sl = SList()
	exp = 0
	res = sl.length()
	assert res == exp


def test_length_2():
	sl = SList([1, 2, 3])
	exp = 3
	res = sl.length()
	assert res == exp


tests_length = [test_length_1, test_length_2]

# -------------------------- #

def test_filter():
	sl = SList([1, 2, 3, 4, 5, 6, 7, 8])
	p = lambda x : x%2 == 0
	res = sl.filter(p)
	for r in res:
		assert p(r)

tests_filter = [test_filter]

# -------------------------- #

def test_empty_true():
	sl = SList()
	exp = True
	res = sl.empty()
	assert res == exp


def test_empty_false():
	sl = SList([1, 2, 3])
	exp = False
	res = sl.empty()
	assert res == exp

tests_empty = [test_empty_true, test_empty_false]

# -------------------------- #

def test_reverse_1():
	sl = SList()
	exp = SList()
	res = sl.reverse()
	assert res == exp


def test_reverse_2():
	sl = SList([1, 2, 3])
	exp = SList([3, 2, 1])
	res = sl.reverse()
	assert res == exp


tests_reverse = [test_reverse_1, test_reverse_2]

# -------------------------- #

def test_map_1():
	sl = SList()
	exp = SList()
	f = lambda x: x
	res = sl.map(f)
	assert res == exp


def test_map_2():
	sl = SList([1, 2, 3])
	exp = SList([2, 3, 4])
	f = lambda x: x + 1
	res = sl.map(f)
	assert res == exp


def test_map_3():
	sl = SList([1, 2, 3])
	exp = SList([1, 2, 3])
	f = lambda x: x
	res = sl.map(f)
	assert res == exp


tests_map = [test_map_1, test_map_2, test_map_3]

# -------------------------- #

def test_flat_map_1():
	sl = SList()
	f = lambda x : range(0, x+1)
	res = sl.flat_map(f)
	exp = SList()
	assert res == exp

def test_flat_map_2():
	sl = SList([1, 2, 3])
	f = lambda x : range(0,x+1)
	res = sl.flat_map(f)
	exp = SList([0, 1, 0, 1, 2, 0, 1, 2, 3])
	assert res == exp

tests_flat_map = [test_flat_map_1, test_flat_map_2]

# -------------------------- #

def test_reduce_1():
	sl = SList()
	f = lambda x,y : x + y
	try:
		res = sl.reduce(f)
		raise Exception("Test failure")
	except EmptyError as e:
		assert True


def test_reduce_2():
	sl = SList([1, 2, 3, 4])
	f = lambda x,y : x + y
	res = sl.reduce(f)
	exp = 10
	assert res == exp

tests_reduce = [test_reduce_1, test_reduce_2]

# -------------------------- #

def test_scan_1():
	c = 0
	sl = SList()
	f = lambda x,y : x + y
	res = sl.scan(f, c)
	exp = SList([0])
	assert res == exp


def test_scan_2():
	c = 0
	sl = SList([1, 2, 3, 4])
	f = lambda x,y : x + y
	res = sl.scan(f, c)
	exp = SList([0, 1, 3, 6])
	assert res == exp

tests_scan = [test_scan_1, test_scan_2]

# -------------------------- #

def test_scan2_1():
	c = 0
	sl = SList()
	f = lambda x,y : x + y
	res = sl.scan2(f, c)
	exp = SList([0])
	assert res == exp


def test_scan2_2():
	c = 0
	sl = SList([1, 2, 3, 4])
	f = lambda x,y : x + y
	res = sl.scan2(f, c)
	exp = SList([9, 7, 4, 0])
	assert res == exp

tests_scan2 = [test_scan2_1, test_scan2_2]

# -------------------------- #

def test_zip_1():
	sl1 = SList()
	sl2 = SList()
	res = sl1.zip(sl2)
	exp = SList()
	assert res == exp


def test_zip_2():
	sl1 = SList([1, 2, 3])
	sl2 = SList([2, 3, 4])
	res = sl1.zip(sl2)
	exp = SList([(1,2),(2,3),(3,4)])
	assert res == exp


def test_zip_3():
	sl1 = SList([1, 2, 3])
	sl2 = SList([2, 3])
	try:
		res = sl1.zip(sl2)
		raise Exception("Test failure")
	except NotEqualSizeError as e:
		assert True


def test_zip_4():
	sl1 = SList([2, 3])
	sl2 = SList([2, 3, 4])
	try:
		res = sl1.zip(sl2)
		raise Exception("Test failure")
	except NotEqualSizeError as e:
		assert True

tests_zip = [test_zip_1, test_zip_2, test_zip_3, test_zip_4]

# -------------------------- #

def test_zipwith_1():
	sl1 = SList()
	sl2 = SList()
	f = lambda x,y : x + y
	res = sl1.zipwith(sl2, f)
	exp = SList()
	assert res == exp


def test_zipwith_2():
	sl1 = SList([1, 2, 3])
	sl2 = SList([2, 3, 4])
	f = lambda x,y : x + y
	res = sl1.zipwith(sl2,f)
	exp = SList([3,5,7])
	assert res == exp


def test_zipwith_3():
	sl1 = SList([1, 2, 3])
	sl2 = SList([2, 3])
	f = lambda x,y : x + y
	try:
		res = sl1.zipwith(sl2,f)
		raise Exception("Test failure")
	except NotEqualSizeError as e:
		assert True


def test_zipwith_4():
	sl1 = SList([2, 3])
	sl2 = SList([2, 3, 4])
	f = lambda x,y : x + y
	try:
		res = sl1.zipwith(sl2,f)
		raise Exception("Test failure")
	except NotEqualSizeError as e:
		assert True

tests_zipwith = [test_zipwith_1, test_zipwith_2, test_zipwith_3, test_zipwith_4]

# -------------------------- #

fcts = tests_head + tests_tail + tests_length + \
	tests_filter + tests_empty + tests_reverse + \
	tests_map + tests_flat_map + tests_reduce + \
	tests_scan + tests_scan2 + tests_zip + tests_zipwith

for f in fcts:
	try :
		f()
		print("\033[32m[OK] " +str(f) + "\033[0m")
	except Exception:
		print("\033[31m[KO] " +str(f)+ "\033[0m")