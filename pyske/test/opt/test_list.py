import pytest
pytestmark = pytest.mark.opt_list
from pyske.core.opt.list import compose, PList, SList
from pyske.core.list.plist import PList as DPList
from pyske.core.list.slist import SList as DSList
from operator import add


def id(x): return x


def incr(x): return x+1


def test_plist():
    exp = DPList.init(id, 10).map(incr).map(incr).reduce(add)
    res = PList.init(id, 10).map(incr).map(incr).reduce(add).run()
    assert res == exp


def test_slist():
    exp = DSList.init(id, 10).map(incr).map(incr).reduce(add)
    res = SList.init(id, 10).map(incr).map(incr).reduce(add).run()
    assert res == exp

