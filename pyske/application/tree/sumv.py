def sumv(tree):
	id = lambda x: x
	add = lambda x,y,z: x + y + z
	return tree.reduce(add, id, add, add, add)
