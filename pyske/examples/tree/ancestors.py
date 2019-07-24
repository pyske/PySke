from pyske.core.util import fun


def plus1(x, y):
	return x + y + 1


def ancestors(tree):
	return tree.map(fun.zero, fun.zero).dacc(plus1, plus1, 0, fun.idt, fun.idt, plus1, plus1)
