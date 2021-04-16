"""
Discrete Fast Fourier Transform
"""

import math
from functools import partial
from pyske.core import PList, par


# ------- Fast Fourier Transform ------------


def _bit_complement(index_k: int, index_i: int) -> int:
    return index_i ^ (1 << index_k)


def _omega(size: int, log2_size: int, index_j: int, index_i: int) -> complex:
    index = index_i >> (log2_size - index_j - 1)
    index_2 = 0
    for _ in range(0, index_j + 1):
        index_2 = 2 * index_2 + 1 if index & 1 else 2 * index_2
        index >>= 1
    value = 2.0 * math.pi / size * (index_2 << (log2_size - index_j - 1))
    return complex(math.cos(value), math.sin(value))


def _combine(size: int, log2_size: int, index_j: int,
             index_i: int, complex_1: complex, complex_2: complex) -> complex:
    # pylint: disable=too-many-arguments
    omega_value = _omega(size, log2_size, index_j, index_i)
    if index_i & (1 << log2_size - index_j - 1):
        return complex_1 + omega_value * complex_2
    return complex_2 + omega_value * complex_1


def fft(input_list: PList[float]) -> PList[complex]:
    # pylint: disable=unsubscriptable-object
    """
    Return the Discrete Fourier Transform.

    Examples::

        >>> from pyske.core import PList
        >>> fft(PList.init(lambda _: 1.0, 128)).to_seq()[0]
        (128+0j)

    :param input_list: a PySke list of floating point numbers
    :return: a parallel list of complex numbers
    """
    size = len(input_list)
    log2_size = int(math.log2(size))
    nprocs = len(par.procs())
    log2_nprocs = int(math.log2(nprocs))
    assert size == 2 ** log2_size
    assert nprocs == 2 ** log2_nprocs
    result = input_list.map(complex)
    for index_j in range(0, log2_nprocs):
        permutation = result.get_partition() \
            .permute(partial(_bit_complement, log2_nprocs - index_j - 1)) \
            .flatten()
        result = permutation.map2i(partial(_combine, size, log2_size, index_j), result)
    for index_j in range(log2_nprocs, log2_size):
        permutation = result.get_partition() \
            .map(lambda l: l.permute(partial(_bit_complement, log2_size - index_j - 1))) \
            .flatten()
        result = permutation.map2i(partial(_combine, size, log2_size, index_j), result)
    return result
