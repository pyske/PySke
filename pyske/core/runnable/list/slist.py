from pyske.core.runnable.etree import ETree, ID_var
from pyske.core.list.slist import SList as SList_core


class SList(ETree):
    """ Class to construct the expression of the computation on a SList_core

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
        if isinstance(value, list) and not isinstance(value, SList_core):
            value = SList_core(value)
        if isinstance(value, SList_core):
            self.value = ID_var
            assert ts is None
            self.children = SList_core([value])
        else:
            self.value = value
            if ts is None:
                self.children = SList_core([])
            else:
                self.children = SList_core(ts)

    def append(self, c):
        return SList(SList_core.__name__, SList_core([SList(self.value, self.children), SList_core.append.__name__, c]))

    def head(self):
        return SList(SList_core.__name__, SList_core([SList(self.value, self.children), SList_core.head.__name__]))

    def tail(self):
        return SList(SList_core.__name__, SList_core([SList(self.value, self.children), SList_core.tail.__name__]))

    def length(self):
        return SList(SList_core.__name__, SList_core([SList(self.value, self.children), SList_core.length.__name__]))

    def filter(self, f):
        return SList(SList_core.__name__, SList_core([SList(self.value, self.children), SList_core.filter.__name__, f]))

    def empty(self):
        return SList(SList_core.__name__, SList_core([SList(self.value, self.children), SList_core.empty.__name__]))

    def reverse(self):
        return SList(SList_core.__name__, SList_core([SList(self.value, self.children), SList_core.reverse.__name__]))

    def map(self, f):
        return SList(SList_core.__name__, SList_core([SList(self.value, self.children), SList_core.map.__name__, f]))

    def map_reduce(self, f, op, e):
        return SList(SList_core.__name__, SList_core([SList(self.value, self.children), SList_core.map_reduce.__name__, f, op, e]))

    def mapi(self, f):
        return SList(SList_core.__name__, SList_core([SList(self.value, self.children), SList_core.mapi.__name__, f]))

    def reduce(self, f, e=None):
        return SList(SList_core.__name__, SList_core([SList(self.value, self.children), SList_core.reduce.__name__, f, e]))

    def scan(self, f, c):
        return SList(SList_core.__name__, SList_core([SList(self.value, self.children), SList_core.scan.__name__, f, c]))

    def scanl(self, f, c):
        return SList(SList_core.__name__, SList_core([SList(self.value, self.children), SList_core.scanl.__name__, f, c]))

    def scanr(self, f):
        return SList(SList_core.__name__, SList_core([SList(self.value, self.children), SList_core.scanr.__name__, f]))

    def scanp(self, f, c):
        return SList(SList_core.__name__, SList_core([SList(self.value, self.children), SList_core.scanp.__name__, f, c]))

    def scanl_last(self, f, c):
        return SList(SList_core.__name__, SList_core([SList(self.value, self.children), SList_core.scanl_last.__name__, f, c]))

    def zip(self, l):
        l1 = SList(l) if not isinstance(l, SList) else l
        return SList(SList_core.__name__, SList_core([SList(self.value, self.children), SList_core.zip.__name__, l1]))

    def map2(self, f, l):
        l1 = SList(l) if not isinstance(l, SList) else l
        return SList(SList_core.__name__, SList_core([SList(self.value, self.children), SList_core.map2.__name__, f, l1]))

    def get_instance(self):
        if self.value == ID_var:
            return self.children[0]
        else:
            return self.children[0].get_instance()

    def run(self):
        # TODO apply optimization
        ch = self.children
        if self.value == ID_var:
            return ch[0]
        else:
            caller = ch[0].run()
            if ch[1] == SList_core.head.__name__:
                return caller.head()
            if ch[1] == SList_core.append.__name__:
                caller.append(ch[2])
                return caller
            if ch[1] == SList_core.tail.__name__:
                return caller.tail()
            if ch[1] == SList_core.length.__name__:
                return caller.length()
            if ch[1] == SList_core.filter.__name__:
                return caller.filter(ch[2])
            if ch[1] == SList_core.empty.__name__:
                return caller.empty()
            if ch[1] == SList_core.reverse.__name__:
                return caller.reverse()
            if ch[1] == SList_core.map.__name__:
                return caller.map(ch[2])
            if ch[1] == SList_core.mapi.__name__:
                return caller.mapi(ch[2])
            if ch[1] == SList_core.reduce.__name__:
                return caller.reduce(ch[2], ch[3])
            if ch[1] == SList_core.map_reduce.__name__:
                return caller.map_reduce(ch[2], ch[3], ch[4])
            if ch[1] == SList_core.scan.__name__:
                return caller.scan(ch[2], ch[3])
            if ch[1] == SList_core.scanl.__name__:
                return caller.scanl(ch[2], ch[3])
            if ch[1] == SList_core.scanr.__name__:
                return caller.scanr(ch[2])
            if ch[1] == SList_core.scanp.__name__:
                return caller.scanp(ch[2], ch[3])
            if ch[1] == SList_core.scanl_last.__name__:
                return caller.scanl_last(ch[2], ch[3])
            if ch[1] == SList_core.zip.__name__:
                arg1 = ch[2].run()
                return caller.zip(arg1)
            if ch[1] == SList_core.map2.__name__:
                arg1 = ch[3].run()
                return caller.map2(ch[2], arg1)
