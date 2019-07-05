from pyske.core.runnable.etree import ETree, ID_var
from pyske.core.tree.btree import BTree as BTree_core
from pyske.core.list.slist import SList


class BTree(ETree):
    """ Class to construct the expression of the computation on a BTree

    ...

    Methods
    -------
    is_leaf()
        Indicates if the BTree is a leaf
    is_node()
        Indicates if the BTree is a node
    map(kl, kn)
        Applies functions to every leaf and to every node values
    mapt(kl, kn)
        Applies kl to every leaf values the current instance, and kn to every subtrees that are nodes
    reduce(k)
        Reduces a BTree into a single value using k
    uacc(k)
        Makes an upward accumulation of the values in a BTree using k
    dacc(gl, gr, c)
        Makes an downward accumulation of the values in a BTree using gl, gr and c
    zip(t)
        Zip the values contained in a second BTree with the ones in the current instance
    map2(f, t)
        Zip the values contained in a tree with the ones in the current instance using a function
    getchl(c)
        Shift all the values contained in the current instance by the left
    getchr(c)
        Shift all the values contained in the current instance by the right
    """

    def __init__(self, value, ts=None):
        if isinstance(value, BTree_core):
            self.value = (ID_var)
            assert ts is None
            self.children = SList([value])
        else:
            self.value = value
            if ts is None:
                self.children = SList([])
            else:
                self.children = SList(ts)

    def get_value(self):
        return BTree(BTree_core.__name__, SList([BTree(self.value, self.children), BTree.get_value.__name__]))

    def set_value(self, v):
        return BTree(BTree_core.__name__, SList([BTree(self.value, self.children), BTree.get_value.__name__, v]))

    def is_leaf(self):
        return BTree(BTree_core.__name__, SList([BTree(self.value, self.children), BTree.is_leaf.__name__]))

    def is_node(self):
        return BTree(BTree_core.__name__, SList([BTree(self.value, self.children), BTree.is_node.__name__]))

    def map(self, kl, kn):
        return BTree(BTree_core.__name__, SList([BTree(self.value, self.children), BTree.map.__name__, kl, kn]))

    def mapt(self, kl, kn):
        return BTree(BTree_core.__name__, SList([BTree(self.value, self.children), BTree.mapt.__name__, kl, kn]))

    def reduce(self, k):
        return BTree(BTree_core.__name__, SList([BTree(self.value, self.children), BTree.reduce.__name__, k]))

    def uacc(self, k):
        return BTree(BTree_core.__name__, SList([BTree(self.value, self.children), BTree.uacc.__name__, k]))

    def dacc(self, gl, gr, c):
        return BTree(BTree_core.__name__, SList([BTree(self.value, self.children), BTree.dacc.__name__, gl, gr, c]))

    def zip(self, t):
        if not isinstance(t, BTree):
            t = BTree(t)
        return BTree(BTree_core.__name__, SList([BTree(self.value, self.children), BTree.zip.__name__, t]))

    def map2(self, f, t):
        if not isinstance(t, BTree):
            t = BTree(t)
        return BTree(BTree_core.__name__, SList([BTree(self.value, self.children), BTree.map2.__name__, f, t]))

    def getchl(self, c):
        return BTree(BTree_core.__name__, SList([BTree(self.value, self.children), BTree.getchl.__name__, c]))

    def getchr(self, c):
        return BTree(BTree_core.__name__, SList([BTree(self.value, self.children), BTree.getchr.__name__, c]))

    def run(self):
        # TODO apply optimization
        ch = self.children
        if self.value == ID_var:
            return ch[0]
        else:
            caller = ch[0].run()
            if ch[1] == BTree_core.set_value.__name__:
                caller.set_value(ch[2])
            if ch[1] == BTree_core.set_value.__name__:
                return caller.get_value()
            if ch[1] == BTree_core.is_leaf.__name__:
                return caller.is_leaf()
            if ch[1] == BTree_core.is_node.__name__:
                return caller.is_node()
            if ch[1] == BTree_core.map.__name__:
                return caller.map(ch[2], ch[3])
            if ch[1] == BTree_core.mapt.__name__:
                return caller.mapt(ch[2], ch[3])
            if ch[1] == BTree_core.reduce.__name__:
                return caller.reduce(ch[2])
            if ch[1] == BTree_core.uacc.__name__:
                return caller.uacc(ch[2])
            if ch[1] == BTree_core.dacc.__name__:
                return caller.dacc(ch[2], ch[3], ch[4])
            if ch[1] == BTree_core.zip.__name__:
                arg1 = ch[2].run()
                return caller.zip(arg1)
            if ch[1] == BTree_core.map2.__name__:
                arg1 = ch[3].run()
                return caller.map2(ch[2], arg1)
            if ch[1] == BTree_core.getchl.__name__:
                return caller.getchl(ch[2])
            if ch[1] == BTree_core.getchr.__name__:
                return caller.getchr(ch[2])


