from typing import Any, TypeVar
import os

from pyske.core import SList
from pyske.core.interface import IOPySke
from pyske.core.io.tree.iodistribution import IODistribution
from pyske.core.io.tree.ioltree import IOLTree
from pyske.core.io.tree.iorltree import IORLTree
from pyske.core.tree.distribution import Distribution
from pyske.core.tree.ptree import PTree
from pyske.core.tree.rptree import RPTree
from pyske.core.support import parallel

_PID: int = parallel.PID

A = TypeVar('A')  # pylint: disable=invalid-name
B = TypeVar('B')  # pylint: disable=invalid-name

__all__ = ['IORPTree']


class IORPTree (IOPySke):

    _EXT_BASE_RPT = "rpt"
    EXT_FILE = _EXT_BASE_RPT + "." + str(_PID)

    @staticmethod
    def split(filename, filename_lt, filename_dist) -> Any:
        if _PID != 0:
            return None

        filename_lt = IORLTree.format_filename(filename_lt)
        filename_dist = IODistribution.format_filename(filename_dist)

        distr = IODistribution.read(filename_dist)

        content_dist = ""
        with open(filename_dist) as fd:
            for line in fd:
                content_dist += line
        fd.close()

        counter_segment = 0
        pid = 0
        with open(filename_lt, "r") as flt:
            content = ""
            for line in flt:
                if line.strip()[0] == '#':
                    continue

                if counter_segment < distr.distribution[pid]:
                    content += line.replace("\n", "") + IOLTree.SEPARATOR_TV
                    counter_segment += 1

                if counter_segment == distr.distribution[pid]:
                    content = content_dist + "\n" + content[:-len(IOLTree.SEPARATOR_TV)]
                    filename_pt = filename + "." + IORPTree._EXT_BASE_RPT + "." + str(pid)
                    with open(filename_pt, "w+") as fpt:
                        fpt.write(content)
                    fpt.close()
                    pid += 1
                    counter_segment = 0
                    content = ""
        flt.close()
        pass

    @staticmethod
    def write(filename, rpt: 'RPTree[A, B]') -> Any:
        filename = IORPTree.format_filename(filename)

        pt = rpt.pt

        str_distr = ""
        for i in range(len(pt.distribution.distribution)):
            d = pt.distribution.distribution[i]
            str_distr += str(d) + (IODistribution.SEPARATOR if i != len(pt.distribution.distribution) - 1 else "")

        str_global_index = ""
        for i in range(len(pt.distribution.global_index)):
            v1, v2 = pt.distribution.global_index[i]
            str_global_index += str(v1) + IODistribution.SEPARATOR_PAIR + str(v2) + \
                                (IODistribution.SEPARATOR if i != len(pt.distribution.global_index) - 1 else "")

        str_content = ""
        for i in range(len(pt.content)):
            val, tag = pt.content[i]
            str_content += (IORLTree.NONE_SYMB if val is None else str(val)) + IOLTree.SEPARATOR_TAG \
                           + IOLTree.str_tag(tag) + (IOLTree.SEPARATOR_TV if i != len(pt.content) - 1 else "")

        with open(filename, "w+") as f:
            content = str_distr + "\n" + str_global_index + "\n" + str_content
            f.write(content)
        f.close()

    @staticmethod
    def read(filename, parser=int) -> 'RPTree[A, B]':
        filename = IORPTree.format_filename(filename)
        dist, global_index = [], []

        content = SList()

        with open(filename, "r") as f:
            count = 0
            for line in f:
                if line.strip()[0] == '#':
                    continue
                if count == 0:
                    str_dists = line.replace("\n", "").split(IODistribution.SEPARATOR)
                    for d in str_dists:
                        dist.append(int(d))
                    count += 1
                elif count == 1:
                    str_gi = line.split(IODistribution.SEPARATOR)
                    for idx in str_gi:
                        idx_temp = idx.split(IODistribution.SEPARATOR_PAIR)
                        global_index.append((int(idx_temp[0]), int(idx_temp[1])))
                    count += 1
                else:
                    l_seg = line.replace("\n", "").split(IOLTree.SEPARATOR_TV)
                    for tv in l_seg:
                        tv_s = tv.split(IOLTree.SEPARATOR_TAG)
                        val = None if tv_s[0] == IORLTree.NONE_SYMB else parser(tv_s[0])
                        tag = IOLTree.parser_tag(tv_s[1])
                        content.append((val, tag))
        f.close()
        return RPTree(PTree.init_bis(content, Distribution(dist, global_index)))

    @staticmethod
    def removeall(filename):
        if filename[-(len(IORPTree._EXT_BASE_RPT) + 1):] != "." + IORPTree._EXT_BASE_RPT:
            filename = filename + "." + IORPTree._EXT_BASE_RPT

        for pid in range(parallel.NPROCS):
            filename_pt = filename + "." + str(pid)
            os.remove(filename_pt)

    @staticmethod
    def remove(filename, ext="rpt." + str(_PID)):
        return super(IORPTree, IORPTree).remove(filename, ext)

    @staticmethod
    def exists(filename, ext="rpt." + str(_PID)):
        return super(IORPTree, IORPTree).exists(filename, ext)

    @staticmethod
    def format_filename(filename, ext="rpt." + str(_PID)):
        return super(IORPTree, IORPTree).format_filename(filename, ext)
