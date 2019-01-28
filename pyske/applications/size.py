from pyske.ltree import LTree

def size(lt):
	id_f = lambda x : x
	sum3 = lambda x,y,z : x + y + z
	mapped_one = lt.map(lambda x:1, lambda x:1)
	return mapped_one.reduce(sum3, id_f, sum3, sum3, sum3)

	