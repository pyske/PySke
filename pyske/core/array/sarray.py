import functools
import array
from pyske.core.list.slist import SList

def code_of_type(x):
    if type(x) == int: return 'i'
    return 'd'

def default(code):
    if code == 'i':
        return 1
    else:
        return 1.0

class SArray(array.array):

    def __default(self):
        return default(self.typecode)

    @staticmethod
    def init(f, size):
        assert 0 <= size
        return SArray(code_of_type(f(0)), [f(i) for i in range(0, size)])

    def is_empty(self):
        """Indicates if a array is empty
        """
        return self.length() == 0


    def length(self):
        """Gives the number of element in the current instance
        """
        return len(self)

    def map(self, f):
        """Applies f to every element of the current instance

        Definition:
        map f [x1, x2, ..., xn] = [f(x1), f(x2), ..., f(xn)]

        Parameters
        ----------
        f : callable
            The function to apply to every values of the current instance
        """
        return SArray(code_of_type(f(self.__default())), [f(x) for x in self])


    def mapi(self, f):
        """Applies f to every index and element of the current instance

        Definition:
        mapi f [x0, x1, ..., xn] = [f(0,x0), f(1,x1), ..., f(n,xn)]

        Parameters
        ----------
        f: callable
        The function to apply to every index and element of the current instance
        """
        return SArray(code_of_type(f(0, self.__default())),
                      [f(i, self[i]) for i in range(0, len(self))])


    def map2(self, f, a):
        assert len(a) == len(self)
        return SArray(code_of_type(f(self.__default(), a.__default())),
                      [f(self[i], a[i]) for i in range(0, len(self))])


    def map2i(self, f, a):
        assert len(a) == len(self)
        return SArray(code_of_type(f(0, self.__default(), a.__default())),
                      [f(i, self[i], a[i]) for i in range(0, len(self))])

    def zip(self, a):
        return SList([(self[i], a(i)) for i in range(0, len(self))])


    def reduce(self, op, e=None):
        assert(not(e is None) or 0 < len(self))
        if e is None:
            return functools.reduce(op, self)
        else:
            return functools.reduce(op, self, e)

    def scan(self, f, c):
        tc = code_of_type(c)
        res = array.array(tc)
        res.append(c)
        for i in range(1, len(self)+1):
            c = f(c, self[i - 1])
            res.append(c)
        return SArray(tc, res)

    def scanl(self, f, c):
        tc = code_of_type(c)
        res = array.array(tc)
        for i in range(0, len(self)):
            res.append(c)
            c = f(c, self[i])
        return SArray(tc, res)

    def scanl_last(self, f, c):
        tc = code_of_type(c)
        res = array.array(tc)
        for i in range(0, len(self)):
            res.append(c)
            c = f(c, self[i])
        return (SArray(tc, res), c)

    def filter(self, p):
        tc = self.typecode
        return SArray(tc, filter(p, self))

