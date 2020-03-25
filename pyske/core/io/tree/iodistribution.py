from typing import Any

from pyske.core.interface import IOPySke
from pyske.core.tree.distribution import Distribution

__all__ = ['IODistribution']


class IODistribution (IOPySke):

    SEPARATOR = ";;"
    SEPARATOR_PAIR = "^"

    @staticmethod
    def write(filename, dist: 'Distribution', ext="dist") -> Any:
        distr, global_index = dist.distribution, dist.global_index

        str_distr = ""
        for i in range(len(distr)):
            d = distr[i]
            str_distr += str(d) + (IODistribution.SEPARATOR if i != len(distr) - 1 else "")

        str_global_index = ""
        for i in range(len(global_index)):
            v1, v2 = global_index[i]
            str_global_index += str(v1) + IODistribution.SEPARATOR_PAIR + str(v2) + \
                                (IODistribution.SEPARATOR if i != len(global_index) - 1 else "")

        content = str_distr + "\n" + str_global_index

        filename = IODistribution.format_filename(filename, ext)
        with open(filename, "w+") as f:
            f.write(content)
        f.close()

    @staticmethod
    def read(filename, ext="dist") -> 'Distribution':
        filename = IODistribution.format_filename(filename, ext)
        assert IODistribution.exists(filename), "Unknown file"
        res_dist = []
        res_gi = []

        with open(filename, "r") as f:
            line_cnt = 0
            for line in f:
                if line.strip()[0] == '#':
                    continue
                if line_cnt is 0:
                    str_dists = line.replace("\n", "").split(IODistribution.SEPARATOR)
                    for d in str_dists:
                        res_dist.append(int(d))
                    line_cnt = 1
                else:
                    str_gi = line.split(IODistribution.SEPARATOR)
                    for idx in str_gi:
                        idx_temp = idx.split(IODistribution.SEPARATOR_PAIR)
                        res_gi.append((int(idx_temp[0]), int(idx_temp[1])))
        f.close()
        return Distribution(res_dist, res_gi)

    @staticmethod
    def remove(filename, ext="dist"):
        return super(IODistribution, IODistribution).remove(filename, ext)

    @staticmethod
    def exists(filename, ext="dist"):
        return super(IODistribution, IODistribution).exists(filename, ext)

    @staticmethod
    def format_filename(filename, ext="dist"):
        return super(IODistribution, IODistribution).format_filename(filename, ext)
