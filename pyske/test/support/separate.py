from pyske.core.tree.ltree import LTree
import argparse

def create_pt_files(lt, n, filename):
	(distribution, global_index) = distribute_tree(lt, n)
	passed_seg = 0
	for pid in range(n):
		nb_segs = distribution[pid]
		filename_pid = filename + "." + str(pid)
		content_pid = ""
		for i_seg in range(passed_seg, passed_seg+ nb_segs):
			content_pid = content_pid + str(lt[i_seg]) + "\n"
		with open(filename_pid,"w+") as f: 
			f.write(str(distribution) + "\n" + str(global_index) + "\n" + content_pid)
		f.close()
		passed_seg += nb_segs


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