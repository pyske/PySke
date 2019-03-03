def size_by_node(tree):
	add = lambda x,y,z: x+y+z
	id = lambda x: x
	tree_mapped= tree.map(lambda x: 1, lambda x: 1)
	return tree_mapped.uacc(add, id, add, add, add)