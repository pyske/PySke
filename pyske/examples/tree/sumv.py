from pyske.core.util import fun


def sum_values(tree):
    return tree.reduce(fun.add, fun.idt, fun.add, fun.add, fun.add)
