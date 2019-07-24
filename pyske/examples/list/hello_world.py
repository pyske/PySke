from pyske.core.list.plist import PList
from pyske.core.list.slist import SList
from pyske.core.util import par


def app(l1, l2):
    return SList(l1 + l2)


msg = "hello world!"
pl1 = PList.init(lambda i: msg[i], len(msg))
pl2 = PList.init(lambda x: x, len(msg))
pl3 = pl1.map(lambda x: x.capitalize())
pl4 = pl3.zip(pl2)
pl5 = pl4.map(lambda x: x[0])
pl6 = pl5.mapi(lambda i, x: (i, x))
pl7 = pl6.map(lambda x: x[1])
pl8 = pl7.map(lambda x: 1)
n = pl8.reduce(lambda x, y: x + y, 0)
pl9 = pl7.get_partition()
pl10 = pl9.map(lambda l: SList(l).filter(lambda c: c != 'O')).flatten()
pl11 = PList.from_seq(["Hello World!"])

filtered = pl10.get_partition().reduce(app, []).reduce(lambda x, y: x + y)
s1 = pl9.reduce(app).reduce(lambda x, y: x + y)
s2 = pl11.to_seq()[0]

par.at_root(lambda:
            print(f'Capitalized: \t{s1}\n'
                  f'Identity:\t{s2}\n'
                  f'Length:\t\t{n}\n'
                  f'Filtered:\t{filtered}'))
