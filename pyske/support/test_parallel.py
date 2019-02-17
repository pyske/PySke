from pyske.support.parallel import *

x = pid
res = scan(lambda x,y:x+y, x)
print("pid=",pid,"\tres=",res)
