from pyske.core.runnable.etree import ETree
from pyske.core.list.slist import SList as Core_SList

import copy

tag_VAR_pattern = "XxXxXxXxXx"


class Rule:
    """
    Describe a transformation rule
    """
    def __init__(self, left, right):
        assert isinstance(left, ETree)
        assert isinstance(right, ETree)
        self.left = left
        self.right = right


class Position(Core_SList):
    """
    SList used to describe a position in a tree
    """
    pass


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

#
# def transformation(t, rules):
#     # TODO return resulting tree
#     test = True
#     while (test):
#         test = False
#         for c in t.children:
#             test = test or transformation(c, rules)
#         for r in rules:
#             if matching(t, r.left):
#                 # TODO Greffer retour rewrite
#                 rewrite(t, r.right)
#                 test = True

