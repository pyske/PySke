from pyske.core.list.plist import PList as PList_core
from pyske.core.list.slist import SList

from pyske.core.runnable.etree import *


class PList(ETree):

    def __init__(self, val=None, ts=None):
        if val is None and ts is None:
            self.value = ID_var
            self.children = SList([PList_core()])
        else:
            if isinstance(val, PList_core):
                self.value = ID_var
                assert ts is None
                self.children = SList([val])
            else:
                if ts is None:
                    self.children = SList([ts])
                else:
                    self.children = SList([])

    @staticmethod
    def init(f, size):
        p = PList_core.init(f, size)
        return PList(val=p)

    @staticmethod
    def from_seq(l):
        p = PList_core.from_seq(l)
        return PList(val=p)

    def to_seq(self):
        return PList(PList_core.__name__, SList([PList(self.value, self.children), PList_core.to_seq.__name__]))

    def length(self):
        return PList(PList_core.__name__, SList([PList(self.value, self.children), PList_core.length.__name__]))

    def map(self, f):
        return PList(PList_core.__name__, SList([PList(self.value, self.children), PList_core.map.__name__, f]))

    def mapi(self, f):
        return PList(PList_core.__name__, SList([PList(self.value, self.children), PList_core.mapi.__name__, f]))

    def map2(self, f, pl):
        pl1 = PList(pl) if not isinstance(pl, PList) else pl
        return PList(PList_core.__name__, SList([PList(self.value, self.children), PList_core.map2.__name__, f, pl1]))

    def zip(self, pl):
        pl1 = PList(pl) if not isinstance(pl, PList) else pl
        return PList(PList_core.__name__, SList([PList(self.value, self.children), PList_core.zip.__name__, pl1]))

    def reduce(self, op, e=None):
        return PList(PList_core.__name__, SList([PList(self.value, self.children), PList_core.reduce.__name__, op, e]))

    def map_reduce(self, f, op, e=None):
        return PList(PList_core.__name__, SList([PList(self.value, self.children), PList_core.map_reduce.__name__, f,
                                                 op, e]))

    def scanr(self, op):
        return PList(PList_core.__name__, SList([PList(self.value, self.children), PList_core.scanr.__name__, op]))

    def scanl(self, op, e):
        return PList(PList_core.__name__, SList([PList(self.value, self.children), PList_core.scanl.__name__, op, e]))

    # def scanl_last(self, op, e):
    #    pass
    #    return p, red

    def get_partition(self):
        return PList(PList_core.__name__, SList([PList(self.value, self.children), PList_core.get_partition.__name__]))

    def flatten(self):
        return PList(PList_core.__name__, SList([PList(self.value, self.children), PList_core.flatten.__name__]))

    def get_instance(self):
        if self.value == ID_var:
            return self.children[0]
        else:
            return self.children[0].get_instance()

    def run(self):
        ch = self.children
        if self.value == ID_var:
            return ch[0]
        else:
            caller = ch[0].run()
            if ch[1] == PList_core.length.__name__:
                return caller.length()
            if ch[1] == PList_core.map.__name__:
                return caller.map(ch[2])
            if ch[1] == PList_core.mapi.__name__:
                return caller.mapi(ch[2])
            if ch[1] == PList_core.reduce.__name__:
                return caller.reduce(ch[2], ch[3])
            if ch[1] == PList_core.scanl.__name__:
                return caller.scanl(ch[2], ch[3])
            if ch[1] == PList_core.scanr.__name__:
                return caller.scanr(ch[2])
            if ch[1] == PList_core.scanl_last.__name__:
                return caller.scanl_last(ch[2], ch[3])
            if ch[1] == PList_core.zip.__name__:
                arg1 = ch[2].run()
                return caller.zip(arg1)
            if ch[1] == PList_core.map2.__name__:
                arg1 = ch[3].run()
                return caller.map2(ch[2], arg1)
