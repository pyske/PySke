import functools
import array

def code_of_type(x):
    if type(x) == int: return 'i'
    return 'd'

def default_of_code(code):
    if code == 'i': return 1
    return 1.0

class SArray(array.array):

    def empty(self):
        """Indicates if a array is empty
        """
        return self.length() == 0

    def head(self):
        """Gives the first element of the current instance
        """
        if self.empty():
            return None
        else:
            return self[0]

    def tail(self):
        """Gives the the current instance without its first element
        """
        return SArray(self.typecode, self[1:])

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
        return SArray(code_of_type(type(f(default_of_code(self.typecode)))), [ f(x) for x in self] )

    def mapi(self, f):
        """Applies f to every index and element of the current instance

        Definition:
        mapi f [x0, x1, ..., xn] = [f(0,x0), f(1,x1), ..., f(n,xn)]

        Parameters
        ----------
        f: callable
        The function to apply to every index and element of the current instance
        """
        return SArray(code_of_type(type(f(default_of_code(self.typecode), 0))),
                                   [f(i, self[i]) for i in range(0, len(self))])