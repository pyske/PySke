import functools


LEFT_LIST = "["
RIGHT_LIST = "]"
SEPARATOR_LIST = ";"


class SList(list):
    """
    An extended definition of lists, including Bird-Meertens Formalism primitives

    ...

    Methods
    -------
    from_str(s, parser):
        Creates a SList from a string
    head()
        Gives the first element of the current instance
    tail()
        Gives the the current instance without its first element
    length()
        Gives the number of element in the current instance
    filter(f)
        Removes all the elements that don't verify a predicate
    empty()
        Indicates if a list is empty
    reverse()
        Reverse a list
    map(f)
        Applies f to every element of the current instance
    mapi(f)
        Applies f to every index and element of the current instance
    reduce(f)
        Reduce the current instance using a reduction function
    scan(f, c)
        Makes an total rightward accumulation of the element on the current instance from an initial value
    scanl(f, c)
        Makes a rightward accumulation of the values from an initial one,
        without considering the last value of the instance
    scanr(f)
        Makes a total leftward accumulation of the values
    scanp(f, c)
         Makes an total lefttward accumulation of the element on the current instance from an initial value
    scanl_last(f, c)
        Makes a rightward accumulation of the values from an initial one,
        considering the last accumulation as an external value
    zip(l)
        Creates a list of pairs from the element of the current instance and another one
    map2(f, l)
        Creates a list of new elements using a function from the element of the current instance and another one
    """

    def __str__(self):
        res = LEFT_LIST
        for i in range(0, self.length()):
            res = res + str(self[i])
            if i != self.length() - 1:
                res = res + SEPARATOR_LIST + " "
        return res + RIGHT_LIST

    @staticmethod
    def from_str(s, parser=int):
        """
        Creates a SList from a string

        Parameters
        ----------
        s : str
            A string representation of the SList
        parser : callable, optional
            A function that transforms a string into a specific type
            By default, string to int
        """
        res = SList([])
        values = s.replace(LEFT_LIST, "").replace(RIGHT_LIST, "").split(SEPARATOR_LIST)
        for v in values:
            res.append(parser(v))
        return res

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
        return SList(self[1:])

    def length(self):
        """Gives the number of element in the current instance
        """
        return len(self)

    def filter(self, p):
        """Removes all the elements that don't verify a predicate

        Parameters
        ----------
        p : callable
            A predicate that all elements in the result must verify
        """
        return SList(filter(p, self))

    def empty(self):
        """Indicates if a list is empty
        """
        return self.length() == 0

    def reverse(self):
        """Reverse a list
        """
        rev = SList()
        for i in range(self.length() - 1, -1, -1):
            rev.append(self[i])
        return rev

    def map(self, f):
        """Applies f to every element of the current instance

        Definition:
        map f [x1, x2, ..., xn] = [f(x1), f(x2), ..., f(xn)]

        Parameters
        ----------
        f : callable
            The function to apply to every values of the current instance
        """
        return SList(map(f, self))

    def mapi(self, f):
        """Applies f to every index and element of the current instance

        Definition:
        mapi f [x0, x1, ..., xn] = [f(0,x0), f(1,x1), ..., f(n,xn)]

        Parameters
        ----------
        f: callable
        The function to apply to every index and element of the current instance
        """
        return SList([f(i, self[i]) for i in range(0, len(self))])

    def map_reduce(self, f, op, e=None):
        """Reduce the current instance using a reduction function

        Definition:
        map_reduce f op [x1, x2, ..., xn] e = op(op(op(e, f x1), ...), f xn)

        Parameters
        ----------
        f : callable
            The used function to reduce the current instance
        e : optional
            Default value for reduction
        """
        if self.empty():
            return e
        else:
            if e is None:
                res = f(self[0])
            else:
                res = op(e, f(self[0]))
            for i in range(1, self.length()):
                res = op(res, f(self[i]))
            return res


    def reduce(self, f, e=None):
        """Reduce the current instance using a reduction function

        Definition:
        reduce f [x1, x2, ..., xn] e = f(f(f(e, x1), ...), xn)

        Parameters
        ----------
        f : callable
            The used function to reduce the current instance
        e : optional
            Default value for reduction
        """
        if e is None:
            return functools.reduce(f, self)
        else:
            return functools.reduce(f, self, e)

    def scan(self, f, c):
        """Makes total a rightward accumulation of the values from an initial one
        The result of scan is a list of size n+1 where n is the size of self.

        Definition:
            scan f c [x_1, x_2, ..., x_n] = [c, f(c, x_1), f(f(c, x_1), x_2), ..., f(f(...,f(f(c, x_1), x_2)), x_n)]

        Parameters
        ----------
        f : callable
            A function to make a new accumulation from the previous accumulation and a current value
        c
            Initial value for the accumulator
        """
        res = self.copy()
        res.append(c)
        res[0] = c
        for i in range(1, len(res)):
            c = f(c, self[i - 1])
            res[i] = c
        return SList(res)

    def scanl(self, f, c):
        """Makes a rightward accumulation of the values from an initial one,
        without considering the last value of the instance
        The result of scanl is a list of size n where n is the size of self.

        Definition:
            scanl f c [] = []
            scanl f c [x_1, x_2, ..., x_n] = [c, f(c, x_1), f(f(c, x_1), x_2), ..., f(f(...,f(f(c, x_1), x_2)), x_n-1)]

        Parameters
        ----------
        f : callable
            A function to make a new accumulation from the previous accumulation and a current value
        c
            Initial value for the accumulator
        """
        res = self.copy()
        for i in range(0, len(res)):
            res[i] = c
            c = f(c, self[i])
        return SList(res)

    def scanr(self, f):
        """Makes a rightward accumulation of the values.

        Definition:
            scanr f [x] = [x]
            scanr f [x_1, x_2, ..., x_n] = [x_1, f(x_1, x_2), ..., f(f(f(x_1, x_2), ...), x_n)]

        Parameters
        ----------
        f : callable
            A function to make a new accumulation from the previous accumulation and a current value
        """
        assert (len(self) > 0)
        res = self.copy()
        c = res[0]
        for i in range(1, len(res)):
            c = f(c, self[i])
            res[i] = c
        return SList(res)

    def scanl_last(self, f, c):
        """Makes a rightward accumulation of the values from an initial one,
        considering the last accumulation as an external value.
        The result of scanl_last is a list of size n where n is the size of self
        and one additional value corresponding to the total accumulation.

        Definition:
            scanl_last f c [] = ([],c)
            scanl_last f c [x_1, x_2, ..., x_n]
                = [c, f(c, x_1), f(f(c, x_1), x_2), ..., f(f(...,f(f(c, x_1), x_2)), x_n-1)]

        Parameters
        ----------
        f : callable
            A function to make a new accumulation from the previous accumulation and a current value
        c
            Initial value for the accumulator
        """
        res = self.scan(f, c)
        last = res.pop()
        return res, last

    def scanp(self, f, c):
        """Makes a leftward accumulation of the values from an initial one.
        The result of scanp is a list of size n where n is the size of self
        and one additional value corresponding to the total accumulation.

        Definition:
            scanp f c [x_1, x_2, ..., x_n] = [f(x_2, f(x_3, f(..., c))), ..., f(x_n, c), c]

        Parameters
        ----------
        f : callable
            A function to make a new accumulation from the previous accumulation and a current value
            Usually, f is associative.
        c
            Initial value for the accumulator.
            Usually, c is the unit of f, i.e. f(x, c) = f(c, x) = x
        """
        res = self.copy()
        for i in range(len(self), 0, -1):
            res[i - 1] = c
            c = f(self[i - 1], c)
        return res

    def zip(self, l):
        """Creates a list of pairs from the element of the current instance and another sequential list

        Precondition
        -------------
        The lengths of self and l should be equal.

        Parameters
        ----------
        l : list
            A list to merge the values of the current instance with
        """
        assert (len(self) == len(l))
        return SList([(x, y) for (x, y) in zip(self, l)])

    def map2(self, f, l):
        """Creates a list of new elements using a function applied to the elements of the current
        instance and another sequential list

        Precondition
        -------------
        The lengths of self and l should be equal.

        Parameters
        ----------
        f : callable
             A function to zip values
        l : list
            The second list to zip with the current instance
        """
        assert (len(self) == len(l))
        return SList([f(x, y) for (x, y) in zip(self, l)])
