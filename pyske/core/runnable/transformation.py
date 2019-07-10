from pyske.core.runnable.etree import ETree
from pyske.core.support.functional import *
from pyske.core.runnable.rule.rule import *

import copy

tag_VAR_pattern = "XxXxXxXxXx"


def matching(tree, pattern):
    """ Test if a pattern and an executing tree are matching

    Parameters
    ----------
    tree : ETree
        A tree that we want to check the matching
    pattern : ETree
        A tree representing an execution pattern

    Returns
    -------
    True if pattern and tree match

    """
    # If the pattern is a non-terminal symbol, everything can match
    if pattern == tag_VAR_pattern:
        return True

    # Check if the classes of the pattern and the tree are the same
    if tree.__class__ == pattern.__class__:
        if isinstance(tree, ETree):
            tc = tree.children
            pc = pattern.children
            # Test if the number of children is the same
            res = (tree.value == pattern.value) and (tc.length() == pc.length())
            # Call of the matching on each children
            for i in range(tc.length()):
                # Test for laziness evaluation
                if not res:
                    return False
                res = res and matching(tc[i], pc[i])
            return res
        else:
            # If the pattern (and the tree) are not a ETree, and the pattern not a VAR_symbol
            # we jsut do an equality test
            return tree == pattern
    return False


def rewrite(tree, pattern):
    def aux_rew(p, f):
        """
        A kind of mapping, but every element is not necessary a ETree

        Parameters
        ----------
        p : ETree | value
            a structure, or a type, whose will be applied a function
        f
            a function to apply
        Returns
        -------
            the initial structure where values have been transformed using f
        """
        tree0 = copy.deepcopy(p)
        if isinstance(tree0, ETree):
            tree0.value = f(tree0.value)
            for c_i in range(len(tree0.children)):
                child = tree0.children[c_i]
                tree0.children[c_i] = aux_rew(child, f)
            return tree0
        else:
            return f(tree0)

    def f(x):
        # The function to apply to every element
        if isinstance(x, Position):
            return get_elem_etree_position(tree, x)
        if isinstance(x, Composition):
            f_args = []
            for pos_f in x.fcts:
                f = get_elem_etree_position(tree, pos_f)
                f_args.append(f)
            return Composition(*f_args)
        else:
            return x
    return aux_rew(pattern, f)


def get_elem_etree_position(t, position):
    # We check we really start from the root of the tree
    assert position[0] == 0
    # Then, according to the previous assertion, t is a tree
    assert isinstance(t, ETree)

    # We will explore t
    # pointer = t

    # Number of coord
    lcd = len(position)
    # Current list of children to explore
    current_ch = [t]

    for i_c in range(lcd):
        coord = position[i_c]
        pointer = current_ch[coord]
        if isinstance(pointer, ETree):
            # equivalent condition: there exist children,
            # or: i_c != lcd-1
            current_ch = pointer.children
    return pointer


def tranformation_aux(tree, rules):
    # not a tree -> no transformation
    if not isinstance(tree, ETree):
        return tree, False

    test = True
    # while the children can be transformed
    while test:
        test = False
        new_child = Core_SList([None] * len(tree.children))
        for child_index in range(len(tree.children)):
            child = tree.children[child_index]
            new_c, test_c = tranformation_aux(child, rules)
            new_child[child_index] = new_c
            test = test or test_c

    tree.children = new_child

    test = True
    while test:
        test = False
        for rule in rules:
            if matching(tree, rule.left):
                tree = rewrite(tree, rule.right)

    return tree, False


def transformation(tree, rules):
    rules = sorted(rules, key=lambda x: x.priority, reverse=True)
    # tree0 = copy.deepcopy(tree)
    res, t = tranformation_aux(tree, rules)
    return res
