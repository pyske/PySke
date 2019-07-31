"""
Tests for the optimization mechanism on lists
"""
from operator import add
import pytest
from pyske.core.opt.list import PList, SList
from pyske.core.list.plist import PList as DPList
from pyske.core.list.slist import SList as DSList
from pyske.core.util.fun import incr, idt

# pylint: disable=invalid-name
pytestmark = pytest.mark.opt_list


def test_plist_constructor():
    # pylint: disable=missing-docstring
    exp = DPList().to_seq()
    res = PList().to_seq().run()
    assert res == exp


def test_slist_constructor():
    # pylint: disable=missing-docstring
    exp = DSList([1, 2, 3])
    res = SList([1, 2, 3]).run()
    assert res == exp


def test_plist():
    # pylint: disable=missing-docstring
    exp = DPList.init(idt, 10).map(incr).map(incr).reduce(add)
    res = PList.init(idt, 10).map(incr).map(incr).reduce(add).run()
    assert res == exp


def test_slist():
    # pylint: disable=missing-docstring
    exp = DSList.init(idt, 10).map(incr).map(incr).reduce(add)
    res = SList.init(idt, 10).map(incr).map(incr).reduce(add).run()
    assert res == exp


def test_plist_with_raw():
    # pylint: disable=missing-docstring
    input_list = DPList.init(idt, 42)
    exp = input_list.map(incr).map(incr).reduce(add)
    res = PList.raw(input_list).map(incr).map(incr).reduce(add).run()
    assert res == exp


def test_slist_with_raw():
    # pylint: disable=missing-docstring
    input_list = DSList.init(idt, 42)
    exp = input_list.map(incr).map(incr).reduce(add)
    res = SList.raw(input_list).map(incr).map(incr).reduce(add).run()
    assert res == exp
