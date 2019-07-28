"""
A module of sequential lists and associated primitives
"""
import functools
from operator import concat
from typing import TypeVar, Callable, Generic, Sequence, Tuple

__all__ = ['SList']

LEFT_LIST = "["
RIGHT_LIST = "]"
SEPARATOR_LIST = ";"

T = TypeVar('T')  # pylint: disable=invalid-name
R = TypeVar('R')  # pylint: disable=invalid-name
U = TypeVar('U')  # pylint: disable=invalid-name


class SList(list, Generic[T]):
    # pylint: disable=too-many-public-methods
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
        Makes an total rightward accumulation of the element on the current instance
        from an initial value
    scanl(f, c)
        Makes a rightward accumulation of the values from an initial one,
        without considering the last value of the instance
    scanr(f)
        Makes a total leftward accumulation of the values
    scanp(f, c)
         Makes an total leftward accumulation of the element on the current instance
         from an initial value
    scanl_last(f, c)
        Makes a rightward accumulation of the values from an initial one,
        considering the last accumulation as an external value
    zip(l)
        Creates a list of pairs from the element of the current instance and another one
    map2(f, l)
        Creates a list of new elements using a function from the element of the current
        instance and another one
    """

    def __str__(self):
        res = LEFT_LIST
        for i in range(0, self.length()):
            res = res + str(self[i])
            if i != self.length() - 1:
                res = res + SEPARATOR_LIST + " "
        return res + RIGHT_LIST

    @staticmethod
    def init(value_at: Callable[[int], T], size: int):
        """
        Creates a list of length ``size``. At index ``idx``,
        the element is ``value_at(idx)``.

        :param value_at: callable
        :param size: int
            size should be positive
        :return: SList
        """
        assert size >= 0
        return SList([value_at(i) for i in range(0, size)])

    @staticmethod
    def from_str(string: str, parser: Callable[[str], U] = int):
        """
        Creates a SList from a string

        Parameters
        ----------
        string : str
            A string representation of the SList
        parser : callable, optional
            A function that transforms a string into a specific type
            By default, string to int
        """
        res = SList([])
        values = string.replace(LEFT_LIST, "").replace(RIGHT_LIST, "").split(SEPARATOR_LIST)
        for val in values:
            res.append(parser(val))
        return res

    def head(self):
        """Gives the first element of the current instance
        """
        if self.empty():
            return None
        return self[0]

    def tail(self):
        """Gives the the current instance without its first element
        """
        return SList(self[1:])

    def length(self) -> int:
        """
        :return: the number of element in the current instance
        """
        return len(self)

    def filter(self, predicate: Callable[[T], bool]):
        """Removes all the elements that don't verify a predicate

        Parameters
        ----------
        predicate: callable
            A predicate that all elements in the result must verify
        """
        return SList(filter(predicate, self))

    def empty(self):
        """Indicates if a list is empty
        """
        return self.length() == 0

    def map(self, unop: Callable[[T], R]):
        """
        Example:

            SList([1, 2, 3]).map(lambda x: x % 2 == 0) == [False, True, False]

        :param unop:
            The function to apply to every values of the current instance
        :return:
            a list obtained by applying the unary function to every element of the current instance

        """
        return SList(map(unop, self))

    def mapi(self, binop: Callable[[int, T], R]):
        """
        Applies f to every index and element of the current instance

        Definition:
        mapi f [x0, x1, ..., xn] = [f(0,x0), f(1,x1), ..., f(n,xn)]

        :param binop
            The function to apply to every index and element of the current instance
        """
        return SList([binop(i, self[i]) for i in range(0, len(self))])

    def map_reduce(self, unop: Callable[[T], R], binop: Callable[[R, R], R], initial=None):
        """Applies f to every index and element of the current instance and then
           reduce the current instance using a reduction operator

        Definition:
        map_reduce f op [x1, x2, ..., xn] e = op(op(op(e, f x1), ...), f xn)

        Parameters
        ----------
        unop : callable
            The function to apply to every values of the current instance
        binop: callable
            The used function to reduce the current instance
        initial : optional
            Default value for reduction
        """
        if self.empty():
            return initial
        if initial is None:
            return functools.reduce(binop, map(unop, self))
        return functools.reduce(binop, map(unop, self), initial)

    def reduce(self, binop: Callable[[T, T], T], initial=None):
        """Reduce the current instance using a reduction function

        Definition:
        reduce f [x1, x2, ..., xn] e = f(f(f(e, x1), ...), xn)

        Parameters
        ----------
        binop: callable
            The used function to reduce the current instance
        initial : optional
            Default value for reduction
        """
        if initial is None:
            return functools.reduce(binop, self)
        return functools.reduce(binop, self, initial)

    def scan(self, binop: Callable[[R, T], R], initial: R):
        """Makes total a rightward accumulation of the values from an initial one
        The result of scan is a list of size n+1 where n is the size of self.

        Definition:
            scan f c [x_1, x_2, ..., x_n] =
              [c, f(c, x_1), f(f(c, x_1), x_2), ..., f(f(...,f(f(c, x_1), x_2)), x_n)]

        Parameters
        ----------
        binop: callable
            A function to make a new accumulation from the previous accumulation and a current value
        initial:
            Initial value for the accumulator
        """
        res: SList[R] = self.copy()
        res.append(initial)
        res[0] = initial
        for i in range(1, len(res)):
            initial = binop(initial, self[i - 1])
            res[i] = initial
        return SList(res)

    def scanl(self, binop: Callable[[R, T], R], initial: R):
        """Makes a rightward accumulation of the values from an initial one,
        without considering the last value of the instance
        The result of scanl is a list of size n where n is the size of self.

        Definition:
            scanl f c [] = []
            scanl f c [x_1, x_2, ..., x_n] =
              [c, f(c, x_1), f(f(c, x_1), x_2), ..., f(f(...,f(f(c, x_1), x_2)), x_n-1)]

        Parameters
        ----------
        binop: callable
            A function to make a new accumulation from the previous accumulation and a current value
        initial:
            Initial value for the accumulator
        """
        res: SList[R] = self.copy()
        for (idx, value) in enumerate(res):
            res[idx] = initial
            initial = binop(initial, value)
        return SList(res)

    def scanr(self, binop):
        """Makes a rightward accumulation of the values.

        Definition:
            scanr f [x] = [x]
            scanr f [x_1, x_2, ..., x_n] = [x_1, f(x_1, x_2), ..., f(f(f(x_1, x_2), ...), x_n)]

        Parameters
        ----------
        binop: callable
            A function to make a new accumulation from the previous accumulation and a current value
        """
        assert self != []
        res = self.copy()
        acc = res[0]
        for idx in range(1, len(res)):
            acc = binop(acc, self[idx])
            res[idx] = acc
        return SList(res)

    def scanl_last(self, binop: Callable[[R, T], R], initial: R):
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
        binop : callable
            A function to make a new accumulation from the previous accumulation and a current value
        initial
            Initial value for the accumulator
        """
        res: SList[R] = self.scan(binop, initial)
        last: R = res.pop()
        return res, last

    def scanp(self, binop, initial):
        """Makes a leftward accumulation of the values from an initial one.
        The result of scanp is a list of size n where n is the size of self
        and one additional value corresponding to the total accumulation.

        Definition:
            scanp f c [x_1, x_2, ..., x_n] = [f(x_2, f(x_3, f(..., c))), ..., f(x_n, c), c]

        Parameters
        ----------
        binop : callable
            A function to make a new accumulation from the previous accumulation and a current value
            Usually, f is associative.
        initial
            Initial value for the accumulator.
            Usually, c is the unit of f, i.e. f(x, c) = f(c, x) = x
        """
        res = self.copy()
        for idx in range(len(self), 0, -1):
            res[idx - 1] = initial
            initial = binop(self[idx - 1], initial)
        return res

    def zip(self, lst: Sequence[U]):
        """Creates a list of pairs from the element of the current instance
        and another sequential list

        Precondition
        -------------
        The lengths of self and lst should be equal.

        Parameters
        ----------
        lst : list
            A list to merge the values of the current instance with
        """
        assert len(self) == len(lst)
        lst: Sequence[Tuple[T, U]] = [(left, right) for (left, right) in zip(self, lst)]
        return SList(lst)

    def map2(self, binop: Callable[[T, U], R], lst: Sequence[U]):
        """Creates a list of new elements using a function applied to the elements of the current
        instance and another sequential list

        Precondition
        -------------
        The lengths of self and lst should be equal.

        Parameters
        ----------
        binop : callable
             A function to zip values
        lst : list
            The second list to zip with the current instance
        """
        assert len(self) == len(lst)
        return SList([binop(left, right) for (left, right) in zip(self, lst)])

    def map2i(self, terop: Callable[[int, T, U], R], lst: Sequence[U]):
        """Creates a list of new elements using a function applied to the elements of the current
        instance and another list as well as their index (first argument)

        Precondition
        -------------
        The lengths of ``self`` and ``lst`` should be equal.

        Parameters
        ----------
        terop : callable
             A function that takes 3 arguments, the first one being an index
        lst : list
            The second list to map with the current instance
        """
        assert len(self) == len(lst)
        return SList([terop(i, self[i], lst[i]) for i in range(0, len(self))])

    def get_partition(self):
        """Returns a list containing the local lists.

        For example if the list is ``[1, 2, 3, 4, 5]`` and it is evenly
        distributed on 2 processors, ```get_partition`` returns
        ``[[1, 2, 3], [4, 5]]``.

        :return: list
        """
        lst: SList[SList[T]] = SList(self)
        return lst

    def flatten(self):
        """Returns a flattened version of ``self``: ``self``
        is supposed to be a list of lists, and ``flatten`` returns
        a list.

        Example: SList([[1, 2], [3, 4]]).flatten() == [1, 2, 3, 4]

        :return: list
        """
        lst: SList[T] = SList(self.reduce(concat, []))
        return lst

    def distribute(self, _: Sequence[int]):
        """
        Returns the same list, but with the new distribution given in argument.
        In sequential, it just returns ``self``.
        :param _: a distribution
        :return: SList
        """
        return self

    def balance(self):
        """
        Returns the same list, but the distribution changes to a
        balanced distribution.
        In sequential, it just returns ``self``.
        :return: SList
        """
        return self
