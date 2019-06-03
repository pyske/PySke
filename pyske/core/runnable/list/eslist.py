from pyske.core.runnable.etree import ETree, ID_var
from pyske.core.list.slist import SList

import hashlib


#TAG_slist =  hashlib.md5(b'slist')

ID_head = hashlib.md5(b'head')
ID_tail = hashlib.md5(b'tail')
ID_length = hashlib.md5(b'length')
ID_filter = hashlib.md5(b'filter')
ID_empty = hashlib.md5(b'empty')
ID_reverse = hashlib.md5(b'reverse')
ID_map = hashlib.md5(b'map')
ID_mapi = hashlib.md5(b'mapi')
ID_reduce = hashlib.md5(b'reduce')
ID_scan = hashlib.md5(b'scan')
ID_scanl = hashlib.md5(b'scanl')
ID_scanr = hashlib.md5(b'scanr')
ID_scanp = hashlib.md5(b'scanp')
ID_scanl_last = hashlib.md5(b'scanl_last')
ID_zip = hashlib.md5(b'zip')
ID_map2 = hashlib.md5(b'map2')


# TODO discuss about: instance.meth1(); instance.meth2(); ...;   V.S   instance.meth1().meth2()...;
# TODO discuss about: should use a tag to describe involved types ? (tag, val)


class ESList(ETree):
    """ Class to construct the expression of the computation on a SList

    ...

    Methods
    -------
    head()
        Gives the first element of the current instance
    tail()
        Gives the the current instance without its first element
    length()
        Gives the number of element in the current instance
    filter(f)
        Removes all the elements that don't verify a predicate
    empty()
        Indicates if a list is empty
    reverse()
        Reverse a list
    map(f)
        Applies f to every element of the current instance
    mapi(f)
        Applies f to every index and element of the current instance
    reduce(f)
        Reduce the current instance using a reduction function
    scan(f, c)
        Makes an total rightward accumulation of the element on the current instance from an initial value
    scanl(f, c)
        Makes a rightward accumulation of the values from an initial one,
        without considering the last value of the instance
    scanr(f)
        Makes a total leftward accumulation of the values
    scanp(f, c)
         Makes an total lefttward accumulation of the element on the current instance from an initial value
    scanl_last(f, c)
        Makes a rightward accumulation of the values from an initial one,
        considering the last accumulation as an external value
    zip(l)
        Creates a list of pairs from the element of the current instance and another one
    map2(f, l)
        Creates a list of new elements using a function from the element of the current instance and another one
    """

    def __init__(self, value, ts=None, strategy=None):
        if isinstance(value, SList):
            self.value = (ID_var)
            assert ts is None
            self.children = SList([value])
        else:
            self.value = value
            if ts is None:
                self.children = SList([])
            else:
                self.children = SList(ts)

    def head(self):
        v = self.value
        ch = self.children
        self.value = None
        self.children = SList([ESList(v, ch), ID_head])

    def tail(self):
        v = self.value
        ch = self.children
        self.value = None
        self.children = SList([ESList(v, ch), ID_tail])

    def length(self):
        v = self.value
        ch = self.children
        self.value = None
        self.children = SList([ESList(v, ch), ID_length])

    def filter(self, f):
        v = self.value
        ch = self.children
        self.value = None
        self.children = SList([ESList(v, ch), ID_filter, f])

    def empty(self):
        v = self.value
        ch = self.children
        self.value = None
        self.children = SList([ESList(v, ch), ID_empty])

    def reverse(self):
        v = self.value
        ch = self.children
        self.value = None
        self.children = SList([ESList(v, ch), ID_reverse])\

    def map(self, f):
        v = self.value
        ch = self.children
        self.value = None
        self.children = SList([ESList(v, ch), ID_map, f])

    def mapi(self, f):
        v = self.value
        ch = self.children
        self.value = None
        self.children = SList([ESList(v, ch), ID_mapi, f])

    def reduce(self, f, e=None):
        v = self.value
        ch = self.children
        self.value = None
        self.children = SList([ESList(v, ch), ID_reduce, f, e])

    def scan(self, f, c):
        v = self.value
        ch = self.children
        self.value = None
        self.children = SList([ESList(v, ch), ID_scan, f, c])

    def scanl(self, f, c):
        v = self.value
        ch = self.children
        self.value = None
        self.children = SList([ESList(v, ch), ID_scanl, f, c])

    def scanr(self, f):
        v = self.value
        ch = self.children
        self.value = None
        self.children = SList([ESList(v, ch), ID_scanr, f])

    def scanp(self, f, c):
        v = self.value
        ch = self.children
        self.value = None
        self.children = SList([ESList(v, ch), ID_scanp, f, c])

    def scanl_last(self, f, c):
        v = self.value
        ch = self.children
        self.value = None
        self.children = SList([ESList(v, ch), ID_scanl_last, f, c])

    def zip(self, l):
        if not isinstance(l, ESList):
            l = ESList(l)
        v = self.value
        ch = self.children
        self.value = None
        self.children = SList([ESList(v, ch), ID_zip, l])

    def map2(self, f, l):
        if not isinstance(l, ESList):
            l = ESList(l)
        v = self.value
        ch = self.children
        self.value = None
        self.children = SList([ESList(v, ch), ID_map2, f, l])


    def run(self):
        # TODO apply optimization
        ch = self.children
        if self.value == ID_var:
            return ch[0]
        else:
            caller = ch[0].run()
            if ch[1] == ID_head:
                return caller.head()
            if ch[1] == ID_tail:
                return caller.tail()
            if ch[1] == ID_length:
                return caller.length()
            if ch[1] == ID_filter:
                return caller.filter(ch[2])
            if ch[1] == ID_empty:
                return caller.empty()
            if ch[1] == ID_reverse:
                return caller.reverse()
            if ch[1] == ID_map:
                return caller.map(ch[2])
            if ch[1] == ID_mapi:
                return caller.mapi(ch[2])
            if ch[1] == ID_reduce:
                return caller.reduce(ch[2], ch[3])
            if ch[1] == ID_scan:
                return caller.scan(ch[2], ch[3])
            if ch[1] == ID_scanl:
                return caller.scanl(ch[2], ch[3])
            if ch[1] == ID_scanr:
                return caller.scanr(ch[2])
            if ch[1] == ID_scanp:
                return caller.scanp(ch[2], ch[3])
            if ch[1] == ID_scanl_last:
                return caller.scanl_last(ch[2], ch[3])
            if ch[1] == ID_zip:
                arg1 = ch[2].run()
                return caller.zip(arg1)
            if ch[1] == ID_map2:
                arg1 = ch[3].run()
                return caller.map2(ch[2], arg1)


