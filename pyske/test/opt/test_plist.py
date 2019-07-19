import pytest
pytestmark = pytest.mark.opt_plist

from pyske.core.opt.plist import PList
from pyske.core.list.plist import PList as DPList
from operator import add

def id(x): return x

def incr(x): return x+1

def test1():
    exp = DPList.init(id, 10).map(incr).map(incr).reduce(add)
    res = PList.init(id, 10).map(incr).map(incr).reduce(add).run()
    assert res == exp
