from pyske.core.util import fun


def size_by_node(tree):
	tree_mapped = tree.map(fun.one, fun.one)
	return tree_mapped.uacc(fun.add, fun.idt, fun.add, fun.add, fun.add)
