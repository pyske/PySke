def ancestors(tree):
	c = 0
	plus1 = lambda c,b : c + b + 1
	id = lambda x : x
	id = lambda x : x
	return tree.map(lambda x:0,lambda x:0).dacc(plus1, plus1, 0, id, id, plus1, plus1)