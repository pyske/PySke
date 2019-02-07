from pyske.ltree import LTree
from pyske.support.separate import create_pt_files

import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-i", help="name of the file that contains the LTree to split")
parser.add_argument("-o", help="name of the files that will contained the PTree (split)")
parser.add_argument("-n", help="how many files we want to get", type=int)
args = parser.parse_args()

filename_in = args.i
filename_out = args.o
n = args.n
if filename_in[-3:] != ".lt":
	filename_in = filename_in + ".lt"

if filename_out[-3:] != ".pt":
	filename_out = filename_out + ".pt"

lt = LTree.init_from_file(filename_in)
create_pt_files(lt, n, filename_out)