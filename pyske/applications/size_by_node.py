from pyske.ltree import LTree

def size_by_node(lt):
	add = lambda x,y,z: x+y+z
	id = lambda x: x
	lt_mapped= lt.map(lambda x: 1, lambda x: 1)
	return lt_mapped.uacc(add, id, add, add, add)