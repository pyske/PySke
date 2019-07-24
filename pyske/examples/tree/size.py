from pyske.core.util import fun
import operator


def size(tree):
	mapped_one = tree.map(fun.one, fun.one)
	return mapped_one.reduce(operator.add, fun.idt, operator.add, operator.add, operator.add)
