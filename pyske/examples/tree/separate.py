"""
Split a linear tree in files.
"""
import argparse
from pyske.core.tree.ltree import LTree
from pyske.core.support.separate import distribute_tree


def _create_pt_files(linear_tree, size, filename):
    (distribution, global_index) = distribute_tree(linear_tree, size)
    passed_seg = 0
    for pid in range(size):
        nb_segs = distribution[pid]
        filename_pid = filename + "." + str(pid)
        content_pid = ""
        for i_seg in range(passed_seg, passed_seg + nb_segs):
            content_pid = content_pid + str(linear_tree[i_seg]) + "\n"
        with open(filename_pid, "w+") as file:
            file.write(str(distribution) + "\n" + str(global_index) + "\n" + content_pid)
        file.close()
        passed_seg += nb_segs


def _main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", help="name of the file that contains the LTree to split")
    parser.add_argument("-o", help="name of the files that will contained the PTree (split)")
    parser.add_argument("-n", help="how many files we want to get", type=int)
    args = parser.parse_args()
    filename_in = args.i
    filename_out = args.o
    numfiles = args.n
    if filename_in[-3:] != ".lt":
        filename_in = filename_in + ".lt"
    if filename_out[-3:] != ".pt":
        filename_out = filename_out + ".pt"
    linear_tree = LTree.init_from_file(filename_in)
    _create_pt_files(linear_tree, numfiles, filename_out)


_main()
