from pyske.ptree import PTree

def ancestors(pt):
	c = 0
	plus1 = lambda c,b : c + 1
	id_f = lambda x : x
	return pt.dacc(plus1, plus1, 0, id_f, id_f, plus1, plus1)