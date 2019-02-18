from pyske.ltree import LTree

def ancestors(lt):
	c = 0
	plus1 = lambda c,b : c + 1
	id_f = lambda x : x
	return lt.dacc(plus1, plus1, 0, id_f, id_f, plus1, plus1)