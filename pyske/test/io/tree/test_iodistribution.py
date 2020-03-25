import random

from pyske.core.io.tree.iodistribution import IODistribution
from pyske.core.tree.distribution import Distribution


def _randint():
    return random.randint(1, 101)


def test_write_read_delete_exists():
    filename = "test"
    dist = [3, 3, 2]
    glob = [(0, 5), (5, 3), (8, 3), (0, 5), (5, 5), (10, 1), (0, 1), (1, 3)]
    exp = Distribution(dist, glob)

    IODistribution.write(filename, exp)
    assert IODistribution.exists(filename)
    res = IODistribution.read(filename)

    assert exp == res
    IODistribution.remove(filename)
    assert not IODistribution.exists(filename)
