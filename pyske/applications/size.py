from pyske.ltree import LTree

def size(lt):
	id = lambda x: x
	add = lambda x,y,z: x + y + z
	mapped_one = lt.map(lambda x:1, lambda x:1)
	return mapped_one.reduce(add, id, add, add, add)

	