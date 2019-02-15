from pyske.ltree import LTree
from pyske.ptree import PTree

from pyske.support.generate import generate_balanced_btree
from pyske.support.parallel import *
from pyske.support.separate import *

from pyske.applications.parallel.prefix import prefix

import time
import random

import sys

# --------------------- #

frdm = lambda : random.randint(1,101)
size = 20
bt = generate_balanced_btree(frdm, size)
lt = LTree.init_from_bt(bt, 3)
filename ="test.pt"
at_root(lambda : create_pt_files(lt, 4, filename))

pt = PTree.init_from_file(filename)
print(pt)

# --------------------- #
time.sleep(2)
# --------------------- #

res = prefix(pt)
print(res.browse())
