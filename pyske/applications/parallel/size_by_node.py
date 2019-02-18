from pyske.ptree import PTree

def size_by_node(pt):
	sum3 = lambda x,y,z : x+y+z
	id_f = lambda x : x
	pt_mapped= pt.map(lambda x : 1, lambda x : 1)
	return pt_mapped.uacc(sum3, id_f, sum3, sum3, sum3)