"""
Sequential array.

Class: SArray
"""
# pylint: disable=missing-docstring
import functools
import array
from pyske.core import SList


def _code_of(value):
    if isinstance(value, int):
        return 'i'
    return 'd'


def _default(code):
    if code == 'i':
        return 1
    return 1.0


class SArray(array.array):

    @staticmethod
    def init(value_at, size):
        assert size >= 0
        return SArray(_code_of(value_at(0)), [value_at(i) for i in range(0, size)])

    def length(self):
        return len(self)

    def map(self, unary_op):
        return SArray(_code_of(unary_op(_default(self.typecode))),
                      [unary_op(x) for x in self])

    def mapi(self, binary_op):
        return SArray(_code_of(binary_op(0, _default(self.typecode))),
                      [binary_op(i, self[i]) for i in range(0, len(self))])

    def map2(self, binary_op, arr):
        assert len(arr) == len(self)
        return SArray(_code_of(binary_op(_default(self.typecode), _default(arr.typecode))),
                      [binary_op(self[i], arr[i]) for i in range(0, len(self))])

    def map2i(self, ternary_op, arr):
        assert len(arr) == len(self)
        return SArray(_code_of(ternary_op(0, _default(self.typecode), _default(arr.typecode))),
                      [ternary_op(i, self[i], arr[i]) for i in range(0, len(self))])

    def zip(self, arr):
        return SList([(self[i], arr[i]) for i in range(0, len(self))])

    def reduce(self, binary_op, neutral=None):
        assert neutral is not None or self
        if neutral is None:
            return functools.reduce(binary_op, self)
        return functools.reduce(binary_op, self, neutral)

    def scan(self, binary_op, neutral):
        toc = _code_of(neutral)
        res = array.array(toc)
        res.append(neutral)
        for idx in range(1, len(self)+1):
            neutral = binary_op(neutral, self[idx - 1])
            res.append(neutral)
        return SArray(toc, res)

    def scanl_last(self, binary_op, neutral):
        toc = _code_of(neutral)
        res = array.array(toc)
        for value in self:
            res.append(neutral)
            neutral = binary_op(neutral, value)
        return SArray(toc, res), neutral

    def scanl(self, binary_op, neutral):
        res, _ = self.scanl_last(binary_op, neutral)
        return res

    def filter(self, predicate):
        toc = self.typecode
        return SArray(toc, filter(predicate, self))
