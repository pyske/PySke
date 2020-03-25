from typing import Any, TypeVar

from pyske.core.interface import IOPySke
from pyske.core.tree.ltree import *
from pyske.core.tree.segment import Segment
from pyske.core.tree.tag import TAG_LEAF, TAG_NODE, TAG_CRITICAL

A = TypeVar('A')  # pylint: disable=invalid-name
B = TypeVar('B')  # pylint: disable=invalid-name

__all__ = ['IOLTree']


class IOLTree (IOPySke):

    SEPARATOR_TAG = "^"
    SEPARATOR_TV = ";;"
    EXT_FILE = "lt"

    @staticmethod
    def parser_tag(tg):
        if tg is "L":
            return TAG_LEAF
        if tg is "N":
            return TAG_NODE
        if tg is "C":
            return TAG_CRITICAL

    @staticmethod
    def str_tag(tg):
        if tg is TAG_LEAF:
            return "L"
        if tg is TAG_NODE:
            return "N"
        if tg is TAG_CRITICAL:
            return "C"

    @staticmethod
    def write(filename, lt: 'LTree[A, B]') -> Any:

        content = ""

        # String creation
        for i in range(lt.length):
            segment = lt[i]
            content_seg = ""
            for j in range(segment.length):
                val, tag = segment[j]
                content_seg += str(val) + IOLTree.SEPARATOR_TAG + IOLTree.str_tag(tag) + \
                               (IOLTree.SEPARATOR_TV if j != segment.length - 1 else "")
            content += content_seg + ("\n" if i != lt.length - 1 else "")

        filename = IOLTree.format_filename(filename)
        with open(filename, "w+") as f:
            f.write(content)
        f.close()

    @staticmethod
    def read(filename, parser=int) -> 'LTree[A, B]':

        filename = IOLTree.format_filename(filename)

        assert IOLTree.exists(filename), "Unknown file"

        res = LTree()

        with open(filename, "r") as f:
            for line in f:
                if line.strip()[0] == '#':
                    continue

                l_seg = line.replace("\n", "").split(IOLTree.SEPARATOR_TV)

                seg = Segment()
                for tv in l_seg:
                    tv_s = tv.split(IOLTree.SEPARATOR_TAG)
                    seg.append((parser(tv_s[0]), IOLTree.parser_tag(tv_s[1])))
                res.append(seg)
        f.close()
        return res

    @staticmethod
    def remove(filename, ext="lt"):
        return super(IOLTree, IOLTree).remove(filename, ext)

    @staticmethod
    def exists(filename, ext="lt"):
        return super(IOLTree, IOLTree).exists(filename, ext)

    @staticmethod
    def format_filename(filename, ext="lt"):
        return super(IOLTree, IOLTree).format_filename(filename, ext)