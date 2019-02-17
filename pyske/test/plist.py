from pyske.errors import NotEqualSizeError, EmptyError, TestFailure
from pyske.test.run import run_tests
from pyske.slist import SList
from pyske.plist import PList
from pyske.support.parallel import *

def app(l1,l2):
    return SList(l1+l2)

msg = "hello world!"

def init_to_seq_empty():
    pl = PList()
    res = pl.to_seq()
    exp = []
    assert res == exp

def init_to_seq_non_empty():
    pl = PList.init(lambda i: msg[i], len(msg))
    res = pl.to_seq()
    exp = list(msg)
    assert res == exp

def map_empty():
    f = lambda x: x.upper()
    input = PList()
    res = input.map(f).to_seq()
    exp = []
    assert res == exp

def map_non_empty():
    f = lambda x: x.upper()
    input = PList.init(lambda i: msg[i], len(msg))
    res = input.map(f).to_seq()
    exp = list(f(msg))
    assert res == exp



fcts = [init_to_seq_empty, init_to_seq_non_empty, map_empty, map_non_empty]

run_ptests(fcts, "plist")