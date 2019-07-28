"""
Tests for the optimization mechanism on lists
"""
from operator import add
import pytest
from pyske.core.opt.list import PList, SList
from pyske.core.list.plist import PList as DPList
from pyske.core.list.slist import SList as DSList
from pyske.core.util.fun import incr

# pylint: disable=invalid-name
pytestmark = pytest.mark.opt_list


def test_plist():
    # pylint: disable=missing-docstring
    exp = DPList.init(id, 10).map(incr).map(incr).reduce(add)
    res = PList.init(id, 10).map(incr).map(incr).reduce(add).run()
    assert res == exp


def test_slist():
    # pylint: disable=missing-docstring
    exp = DSList.init(id, 10).map(incr).map(incr).reduce(add)
    res = SList.init(id, 10).map(incr).map(incr).reduce(add).run()
    assert res == exp
