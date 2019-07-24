import pytest
from pyske.core.opt.list import PList, SList
from pyske.core.list.plist import PList as DPList
from pyske.core.list.slist import SList as DSList
from operator import add
from pyske.core.util.fun import incr

pytestmark = pytest.mark.opt_list


def test_plist():
    exp = DPList.init(id, 10).map(incr).map(incr).reduce(add)
    res = PList.init(id, 10).map(incr).map(incr).reduce(add).run()
    assert res == exp


def test_slist():
    exp = DSList.init(id, 10).map(incr).map(incr).reduce(add)
    res = SList.init(id, 10).map(incr).map(incr).reduce(add).run()
    assert res == exp
