from pyske.ltree import LTree
from pyske.support.separate import create_pt_files

import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-f", help="name of the file that contains the LTree to split")
parser.add_argument("-n", help="how many files we want to get", type=int)
args = parser.parse_args()

filename = args.f
n = args.n
if filename[-3:] == ".lt":
	filename_lt = filename
	filename_pt = filename[:-3] + ".pt"
else :
	filename_lt = filename + ".lt"
	filename_pt = filename + ".pt"


lt = LTree.init_from_file(filename_lt)
create_pt_files(lt, n, filename_pt)