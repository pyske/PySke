from typing import Any, TypeVar

from pyske.core.interface import IOPySke
from pyske.core.io.tree import IOLTree
from pyske.core.tree import RLTree
from pyske.core.tree.ltree import *
from pyske.core.tree.segment import Segment

A = TypeVar('A')  # pylint: disable=invalid-name
B = TypeVar('B')  # pylint: disable=invalid-name

__all__ = ['IORLTree']


class IORLTree (IOPySke):

    EXT_FILE = "rlt"
    NONE_SYMB = "_"

    @staticmethod
    def write(filename, rt: 'RLTree[A, B]') -> Any:
        lt = rt.lt
        content = ""

        # String creation
        for i in range(lt.length):
            segment = lt[i]
            content_seg = ""
            for j in range(segment.length):
                val, tag = segment[j]
                str_val = IORLTree.NONE_SYMB if val is None else str(val)
                content_seg += str_val + IOLTree.SEPARATOR_TAG + IOLTree.str_tag(tag) + \
                               (IOLTree.SEPARATOR_TV if j != segment.length - 1 else "")
            content += content_seg + ("\n" if i != lt.length - 1 else "")

        filename = IORLTree.format_filename(filename)
        with open(filename, "w+") as f:
            f.write(content)
        f.close()

    @staticmethod
    def read(filename, parser=int) -> 'RLTree[A, B]':
        filename = IORLTree.format_filename(filename)
        assert IORLTree.exists(filename), "Unknown file"

        res = LTree()

        with open(filename, "r") as f:
            for line in f:
                if line.strip()[0] == '#':
                    continue

                l_seg = line.replace("\n", "").split(IOLTree.SEPARATOR_TV)
                seg = Segment()

                for tv in l_seg:
                    tv_s = tv.split(IOLTree.SEPARATOR_TAG)
                    val = None if tv_s[0] == IORLTree.NONE_SYMB else parser(tv_s[0])
                    tag = IOLTree.parser_tag(tv_s[1])
                    seg.append((val, tag))
                res.append(seg)
        f.close()
        return RLTree(res)

    @staticmethod
    def remove(filename, ext="rlt"):
        return super(IORLTree, IORLTree).remove(filename, ext)

    @staticmethod
    def exists(filename, ext="rlt"):
        return super(IORLTree, IORLTree).exists(filename, ext)

    @staticmethod
    def format_filename(filename, ext="rlt"):
        return super(IORLTree, IORLTree).format_filename(filename, ext)

