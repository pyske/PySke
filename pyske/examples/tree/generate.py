"""
Generation of a binary tree
"""

import argparse
import random

from pyske.core.support.generate import balanced_btree, random_btree, ill_balanced_btree
from pyske.core.tree.ltree import LTree

RDM = 'rdm'
BAL = 'bal'
ILL = 'ill'
CHOICES = [RDM, BAL, ILL]


def _randint(_):
    # pylint: disable=missing-docstring
    return random.randint(1, 101)


def _main():
    # pylint: disable=missing-docstring
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", help="name of the file to create to store the BTree")
    parser.add_argument("-s", help="size of BTree to generate", type=int)
    parser.add_argument("-t", help="type of BTree to generate", choices=CHOICES)
    parser.add_argument("-m", help="m value for serialization", type=int)
    args = parser.parse_args()
    filename = args.f
    num_m = args.m
    size = args.s
    if filename[-3:] != ".lt":
        filename = filename + ".lt"
    type_bt = args.t
    if type_bt not in CHOICES:
        raise Exception("Not a valid type of tree")
    btr = None
    if type_bt == RDM:
        btr = random_btree(_randint, size)
    if type_bt == BAL:
        btr = balanced_btree(_randint, size)
    if type_bt == ILL:
        btr = ill_balanced_btree(_randint, size)
    LTree.init_from_bt(btr, num_m).write_file(filename)


_main()
