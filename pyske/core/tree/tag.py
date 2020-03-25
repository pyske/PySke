from abc import abstractmethod
from typing import TypeVar
from pyske.core.util.fun import up_div, dist_euclidean

__all__ = ['TAG_LEAF', 'TAG_NODE', 'TAG_CRITICAL', 'Tag']
   
TAG_LEAF = 1
TAG_NODE = 2
TAG_CRITICAL = 3

A = TypeVar('A')  # pylint: disable=invalid-name
B = TypeVar('B')  # pylint: disable=invalid-name


class Tag:

    @staticmethod
    def mbridge(bt: 'BTree[A, B]', m: int = 1):
        def k_mapt(l, b, r):
            size_l, _ = l
            size_r, _ = r

            if up_div(b, m) > up_div(size_l, m) and up_div(b, m) > up_div(size_r, m):
                return b, TAG_CRITICAL
            else:
                return b, TAG_NODE

        bt_one = bt.map(lambda x: 1, lambda x: 1)
        bt_size = bt_one.uacc(lambda x, y, z: x + y + z)
        bt_temp = bt_size.map(lambda x: (x, TAG_LEAF), lambda x: x)
        bt_tagged_acc = bt_temp.uacc(k_mapt)
        bt_tags = bt_tagged_acc.map(lambda x: x[1], lambda x: x[1])
        bt_val = bt.map2(lambda x, y: (x, y), lambda x, y: (x, y), bt_tags)
        return bt_val

    @staticmethod
    def avg(bt: 'BTree[A, B]', m: int = 1):
        avg_size = bt.size / m

        def _k(l, b, r):
            (acc_size_left, _, has_crit_left) = l
            (acc_size_right, _, has_crit_right) = r

            acc_size = 1 + acc_size_left + acc_size_right

            is_crit = (has_crit_left and has_crit_right) \
                      or dist_euclidean(acc_size, avg_size) > dist_euclidean(acc_size_left, avg_size) \
                      or dist_euclidean(acc_size, avg_size) > dist_euclidean(acc_size_right, avg_size)
            has_crit = has_crit_left or has_crit_right or is_crit
            return acc_size, is_crit, has_crit

        def _kl(_):
            return TAG_LEAF

        def _kn(x):
            return TAG_CRITICAL if x[1] else TAG_NODE

        bt_tags = bt.map(lambda x: (1, False, False), lambda x: (1, False, False)).uacc(_k).map(_kl, _kn)
        return bt.map2(lambda x, y: (x, y), lambda x, y: (x, y), bt_tags)
