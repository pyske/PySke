from pyske.support.generate import generate_balanced_btree, generate_random_btree, generate_illbalanced_btree
from pyske.ltree import LTree
import random
import argparse
import math

# --------------------- #

parser = argparse.ArgumentParser()
parser.add_argument("-f", help="name of the file to create to store the BTree")
parser.add_argument("-s", help="size of BTree to generate", type=int)
parser.add_argument("-t", help="type of BTree to generate")
parser.add_argument("-m", help="m value for serialization", type=int)
args = parser.parse_args()

# --------------------- #

filename = args.f
if filename[-3:] != ".lt":
	filename = filename + ".lt"

type_bt = args.t
if type_bt != "rdm" and type_bt != "bal" and type_bt != "ill" :
	raise Exception("Not a valid type of tree") 

size = args.s

# --------------------- #

frdm = lambda : random.randint(1,101)

if type_bt == "rdm" :
	bt = generate_random_btree(frdm, size)

if type_bt == "bal" :
	bt = generate_balanced_btree(frdm, size)

if type_bt == "ill" :
	bt = generate_illbalanced_btree(frdm, size)

# --------------------- #

m = args.m
lt = LTree.init_from_bt(bt, m)
lt.write_file(filename)


