from pyske.plist import PList
from pyske.support.parallel import *

msg = "hello world!"
pl1 = PList.init(lambda i: msg[i], len(msg))
pl2 = PList.init(lambda x: x, len(msg))
pl3 = pl1.map(lambda x: x.capitalize())
pl4 = pl3.zip(pl2)
pl5 = pl4.map(lambda x: x[0])
pl6 = pl5.mapi(lambda i,x: (i,x))
pl7 = pl6.map(lambda x: x[1])
pl8 = pl7.map(lambda x: 1)
n = pl8.reduce(lambda x,y:x+y, 0)
pl9 = pl7.get_partition()
l = SList(pl9.reduce(lambda x,y: x+y)).reduce(lambda x,y: x+y)
at_root(lambda: print(l, "\nLength: ",n))