from pyske.ltree import LTree

def size_by_node(lt):
	sum3 = lambda x,y,z : x+y+z
	id_f = lambda x : x
	lt_mapped= lt.map(lambda x : 1, lambda x : 1)
	return lt_mapped.uacc(sum3, id_f, sum3, sum3, sum3)