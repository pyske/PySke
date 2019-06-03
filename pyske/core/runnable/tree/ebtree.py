from pyske.core.runnable.etree import ETree, ID_var
from pyske.core.tree.btree import BTree
from pyske.core.list.slist import SList

import hashlib

ID_is_leaf = hashlib.md5(b'is_leaf')
ID_is_node = hashlib.md5(b'is_node')
ID_map = hashlib.md5(b'map')
ID_mapt = hashlib.md5(b'mapt')
ID_reduce = hashlib.md5(b'reduce')
ID_uacc = hashlib.md5(b'uacc')
ID_dacc = hashlib.md5(b'dacc')
ID_zip = hashlib.md5(b'zip')
ID_map2 = hashlib.md5(b'map2')
ID_getchl = hashlib.md5(b'getchl')
ID_getchr = hashlib.md5(b'getchr')


# TODO discuss about: instance.meth1(); instance.meth2(); ...;   V.S   instance.meth1().meth2()...;
# TODO discuss about: should use a tag to describe involved types ? (tag, val)


class EBTree(ETree):
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

    def __init__(self, value, ts=None, strategy=None):
        if isinstance(value, BTree):

            self.value = (ID_var)
            assert ts is None
            self.children = SList([value])
        else:
            self.value = value
            if ts is None:
                self.children = SList([])
            else:
                self.children = SList(ts)

    def is_leaf(self):
        v = self.value
        ch = self.children
        self.value = None
        self.children = SList([EBTree(v, ch), ID_is_leaf])

    def is_node(self):
        v = self.value
        ch = self.children
        self.value = None
        self.children = SList([EBTree(v, ch), ID_is_node])

    def map(self, kl, kn):
        v = self.value
        ch = self.children
        self.value = None
        self.children = SList([EBTree(v, ch), ID_map, kl, kn])

    def mapt(self, kl, kn):
        v = self.value
        ch = self.children
        self.value = None
        self.children = SList([EBTree(v, ch), ID_mapt, kl, kn])

    def reduce(self, k):
        v = self.value
        ch = self.children
        self.value = None
        self.children = SList([EBTree(v, ch), ID_reduce, k])

    def uacc(self, k):
        v = self.value
        ch = self.children
        self.value = None
        self.children = SList([EBTree(v, ch), ID_uacc, k])

    def dacc(self, gl, gr, c):
        v = self.value
        ch = self.children
        self.value = None
        self.children = SList([EBTree(v, ch), ID_dacc, gl, gr, c])

    def zip(self, t):
        if not isinstance(t, EBTree):
            t = EBTree(t)
        v = self.value
        ch = self.children
        self.value = None
        self.children = SList([EBTree(v, ch), ID_zip, t])

    def map2(self, f, t):
        if not isinstance(t, EBTree):
            t = EBTree(t)
        v = self.value
        ch = self.children
        self.value = None
        self.children = SList([EBTree(v, ch), ID_map2, t, f])

    def getchl(self, c):
        v = self.value
        ch = self.children
        self.value = None
        self.children = SList([EBTree(v, ch), ID_getchl, c])

    def getchr(self, c):
        v = self.value
        ch = self.children
        self.value = None
        self.children = SList([EBTree(v, ch), ID_getchr, c])

    def run(self):
        # TODO apply optimization
        ch = self.children
        if self.value == ID_var:
            return ch[0]
        else:
            caller = ch[0].run()
            if ch[1] == ID_is_leaf:
                return caller.is_leaf()
            if ch[1] == ID_is_node:
                return caller.is_node()
            if ch[1] == ID_map:
                return caller.map(ch[2], ch[3])
            if ch[1] == ID_mapt:
                return caller.mapt(ch[2], ch[3])
            if ch[1] == ID_reduce:
                return caller.reduce(ch[2])
            if ch[1] == ID_uacc:
                return caller.uacc(ch[2])
            if ch[1] == ID_dacc:
                return caller.dacc(ch[2], ch[3], ch[4])
            if ch[1] == ID_zip:
                arg1 = ch[2].run()
                return caller.zip(arg1)
            if ch[1] == ID_map2:
                arg1 = ch[2].run()
                return caller.map2(ch[3], arg1)
            if ch[1] == ID_getchl:
                return caller.getchl(ch[2])
            if ch[1] == ID_getchr:
                return caller.getchr(ch[2])


