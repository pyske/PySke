import sys
from pyske.core.support.errors import EmptyError, NotEqualSizeError, UnknownTypeError, IllFormedError, ApplicationError, \
    NotSameTagError
from pyske.core.list.slist import SList
from pyske.core.tree.btree import BTree, Leaf, Node

MINUS_INFINITY = int((-sys.maxsize - 1) / 2)
VTag_LEAF = 1
VTag_NODE = 2
VTag_CRITICAL = 3

SEPARATOR_TV = "^"
LEFT_TV = "("
RIGHT_TV = ")"
LEFT_SEG = "["
RIGHT_SEG = "]"
SEPARATOR_SEG = ";"
EXT_FILE_LT = "lt"


def parseVTag(vt):
    """
    Get a VTag from a label

    Parameters
    ----------
    t : str
        A label that we want to get the VTag

    Raises
    ------
    UnknownTypeError
        If the label is not known in VTag
    """
    vt = vt.strip()
    if vt == "C":
        return VTag_CRITICAL
    if vt == "L":
        return VTag_LEAF
    if vt == "N":
        return VTag_NODE

    raise UnknownTypeError('Type of value unknown: ' + str(vt))


class TaggedValue:
    """
    A class used to represent a Value in a linearized tree

    ...

    Attributes
    ----------
    val:
        A value describing the current element
    type: VTag

    Methods
    -------
    getVTag()
        Get the VTag value used to describe the tag of the current instance
    getVTagEnum()
        Get the VTag tag of the current instance
    getValue()
        Get the value contained in the current instance
    is_leaf()
        Indicates if the current instance is tagged by the Leaf VTag
    is_critical()
        Indicates if the current instance is tagged by the Critical VTag
    is_node()
        Indicates if the current instance is tagged by the Node VTag
    """

    def __init__(self, val, t):
        self.val = val
        if (t == VTag_LEAF) | (t == VTag_NODE) | (t == VTag_CRITICAL):
            self.tag = t
        else:
            try:
                self.tag = parseVTag(t)
            except UnknownTypeError as e:
                print(str(e))

    def __str__(self):
        def tag2str(tag):
            if tag == VTag_CRITICAL:
                return "C"
            if tag == VTag_LEAF:
                return "L"
            if tag == VTag_NODE:
                return "N"

        return LEFT_TV + str(self.val) + SEPARATOR_TV + tag2str(self.tag) + RIGHT_TV

    def __eq__(self, other):
        if isinstance(other, TaggedValue):
            return (self.tag == other.tag) and (self.val == other.val)
        return False

    def get_tag(self):
        """
        Get the VTag value used to describe the tag of the current instance
        """
        return self.tag

    def get_value(self):
        """
        Get the VTag tag of the current instance
        """
        return self.val

    def is_leaf(self):
        """
        Indicates if the current instance is tagged by the Leaf VTag
        """
        return self.tag == VTag_LEAF

    def is_critical(self):
        """
        Indicates if the current instance is tagged by the Critical VTag
        """
        return self.tag == VTag_CRITICAL

    def is_node(self):
        """
        Indicates if the current instance is tagged by the Node VTag
        """
        return self.tag == VTag_NODE


class Segment(SList):
    """
    A list of TaggedValue

    Methods
    -------
    has_critical()
        Indicates if the current instance contains a value tagged by the Critical VTag
    map_local(kl, kn)
        Applies function kl to each leaf and function kn to each internal node and the m-critical node in a local Segment
    reduce_local(k, phi, psi_l, psi_r)
        Reduces a local Segment into a value
    reduce_global(psi_n)
        Makes a global reduction using local reductions of Segments
    uacc_local(k, phi, psi_l, psi_r)
        Computes local upwards accumulation and reduction.
    uacc_global(psi_n)
        Performs sequential upwards accumulation
    uacc_update(seg, k, lc, rc)
        Makes an update of the current accumulation, using initial values and the top accumulated values
    dacc_path(phi_l, phi_r, psi_u)
        Finds the m-critical node and then computes two values only on the path from the root node to the m-critical node
    dacc_global(psi_d, c)
        Performs sequential downwards accumulation
    dacc_local(gl, gr, c)
        Computes local downward accumulation for the current instance using an accumulative parameter resulting of a global downward accumulation
    from_str(s, parser)
        Get a segment from a string value
    """

    def __eq__(self, other):
        if isinstance(other, Segment):
            if self.length() != other.length():
                return False
            for i in range(0, self.length()):
                if self[i] != other[i]:
                    return False
            return True
        return False

    def has_critical(self):
        """
        Indicates if the current instance contains a value tagged by the Critical VTag
        """
        for v in self:
            if v.is_critical():
                return True
        return False

    def map_local(self, kl, kn):
        """
        Applies function kl to each leaf and function kn to each internal node and the m-critical node in a local Segment

        Parameters
        ----------
        kl : lambda x -> y
            The function to apply to every values tagged by LEAF of the current instance
        kn : lambda x -> y
            The function to apply to every values tagged by CRITICAL or NODE of the current instance
        """
        res = Segment()
        for tv in self:
            if tv.is_leaf():
                v = TaggedValue(kl(tv.get_value()), tv.get_tag())
            else:  # v.is_node() or v.is_critical()
                v = TaggedValue(kn(tv.get_value()), tv.get_tag())
            res.append(v)
        return res

    def reduce_local(self, k, phi, psi_l, psi_r):
        """
        Reduces a local Segment into a value

        Parameters
        ----------
        k : lambda x,y,z -> r
            The function used to reduce a BTree into a single value
        phi : lambda x -> y
            A function used to respect the closure property
        psi_l : lambda x,y,z -> r
            A function used to respect the closure property to make partial computation on the left
        psi_r : lambda x,y,z -> r
            A function used to respect the closure property to make partial computation on the right

        Raises
        ------
        EmptyError:
            If the current instance is empty
        IllFormedError:
            If the current instance does not represent a correct linearized subtree
            That is there is a node that does not have two children which can be either a leaf value or a critical value
        """
        if self.is_empty():
            raise EmptyError("reduce_local cannot be applied to an empty Segment")
        stack = []
        d = MINUS_INFINITY
        has_critical = False
        for v in self.reverse():
            # Starts by the end, that is the most deep leaves
            # We stack every elements we already reduced
            if v.is_leaf():
                # We cannot reduce a leaf value
                stack.append(v.get_value())
                d = d + 1
            elif v.is_node():
                if len(stack) < 2:
                    raise IllFormedError(
                        "reduce_local cannot be applied if there is a node that does not have two children in the current instance")
                # We get two sub-reductions to make a reduction with the current node value
                lv = stack.pop()
                rv = stack.pop()
                if d == 0:
                    # The current node is an ancestor of a critical value by the left
                    # That is, there is a critical value on its left children in a BTree representation
                    # We process and stack a partial reduction
                    stack.append(psi_l(lv, phi(v.get_value()), rv))
                elif d == 1:
                    # The current node is an ancestor of a critical value by the right
                    # That is, there is a critical value on its right children in a BTree representation
                    # We process and stack a partial reduction
                    stack.append(psi_r(lv, phi(v.get_value()), rv))
                    d = 0
                else:
                    # We did not meet a critical value, we process and stack a normal reduction
                    stack.append(k(lv, v.get_value(), rv))
            else:  # v.is_critical()
                # we process and stack the reduction of critical value
                stack.append(phi(v.get_value()))
                has_critical = True
                d = 0
        top = stack.pop()
        if has_critical:
            # The current instance represented a node in the global structure of a linearized tree
            return TaggedValue(top, "N")
        else:
            # The current instance represented a leaf in the global structure of a linearized tree
            return TaggedValue(top, "L")

    def reduce_global(self, psi_n):
        """
        Makes a global reduction using local reductions of Segments

        Parameters
        ----------
        psi_n : lambda x,y,z -> r
            A function used to respect the closure property on k (the initial function used for reduction) to allow partial computation

        Raises
        ------
        EmptyError:
            If the current instance is empty
        IllFormedError:
            If the current instance does not represent a list of top values of a correct list of subtrees
            That is for each node, there is not exist two children, of there is a critical value in the current instance
        """
        if self.has_critical():
            raise ApplicationError("reduce_global cannot be applied to a Segments which contains a critical")
        if self.is_empty():
            raise EmptyError("reduce_global cannot be applied to an empty Segment")
        stack = []
        for g in self.reverse():
            # We stack every value we already reduced
            if g.is_leaf():
                # Nothing to calculate, we only stack the value
                stack.append(g.get_value())
            else:  # g.is_node()
                # We get two sub reductions to make a total reduction of the current node
                if len(stack) < 2:
                    raise IllFormedError(
                        "reduce_global cannot be applied if there is a node that does not have two children in the current instance")
                lv = stack.pop()
                rv = stack.pop()
                # We process and stack a reduction
                stack.append(psi_n(lv, g.get_value(), rv))
        top = stack.pop()
        return top

    def uacc_local(self, k, phi, psi_l, psi_r):
        """
        Computes local upwards accumulation and reduction

        Parameters
        ----------
        k : lambda x,y,z -> r
            The function used to reduce a BTree into a single value
        phi : lambda x -> y
            A function used to respect the closure property
        psi_l : lambda x,y,z -> r
            A function used to respect the closure property to make partial computation on the left
        psi_r : lambda x,y,z -> r
            A function used to respect the closure property to make partial computation on the right

        Raises
        ------
        EmptyError:
            If the current instance is empty
        IllFormedError:
            If the current instance does not represent a correct linearized subtree
            That is there is a node that doesn't have two children which can be either a leaf value or a critical value
        """

        if self.is_empty():
            raise EmptyError("uacc_local cannot be applied to an empty Segment")
        stack = []
        d = MINUS_INFINITY
        res = Segment()
        has_crit = False

        for v in self.reverse():
            # We stack all the values of previous accumulation
            if v.is_leaf():
                res.insert(0, v)
                stack.append(v.get_value())
                d = d + 1

            elif v.is_node():
                if len(stack) < 2:
                    raise IllFormedError(
                        "uacc_local cannot be applied if there is a node that does not have two children in the current instance")
                # We get the values of two sub upward accumulation
                lv = stack.pop()
                rv = stack.pop()
                if d == 0:
                    # The current node is an ancestor of a critical value by the left
                    # That is, there is a critical value on its left children in a BTree representation
                    # We process and stack the value of a partial accumulation
                    val = phi(v.get_value())
                    stack.append(psi_l(lv, val, rv))
                    res.insert(0, None)
                elif d == 1:
                    # The current node is an ancestor of a critical value by the left
                    # That is, there is a critical value on its left children in a BTree representation
                    # We process and stack the value of a partial accumulation
                    val = phi(v.get_value())
                    stack.append(psi_r(lv, val, rv))
                    res.insert(0, None)
                    d = 0
                else:
                    # We did not meet a critical value, we can process a normal upward accumulation with k
                    val = k(lv, v.get_value(), rv)
                    res.insert(0, TaggedValue(val, v.get_tag()))
                    stack.append(val)
                    d = d - 1

            else:  # v.is_critical()
                # The current value is critical. We make a partial accumulation with phi and stack the result
                stack.append(phi(v.get_value()))
                res.insert(0, None)
                d = 0
                has_crit = True

        top = stack.pop()
        tag = "N" if has_crit else "L"
        # We return both the top values for following global upward accumulation, and the current accumulated subtree
        return (TaggedValue(top, tag), res)

    def uacc_global(self, psi_n):
        """
        Performs sequential upwards accumulation

        Parameters
        ----------
        psi_n : lambda x,y,z -> r
            A function used to respect the closure property on k (the initial function used for accumulation) to allow partial computation

        Raises
        ------
        ApplicationError:
            If the current instance contains a critical value
        IllformedError:
            If the current instance does not represent a correct linearized subtree
            That is there is a node that doesn't have two children
        """

        stack = []
        res = Segment()
        if self.has_critical():
            raise ApplicationError("uacc_global cannot be applied to a Segments which contains a critical")
        for g in self.reverse():
            # We process a global accumulation using a stack to store previous accumulation, to get them for the accumulation on nodes
            if g.is_leaf():
                res.insert(0, g)
                val = g.get_value()
            else:  # g.is_node()
                if len(stack) < 2:
                    raise IllFormedError(
                        "uacc_global cannot be applied if there is a node that does not have two children in the current instance")
                lv = stack.pop()
                rv = stack.pop()
                val = psi_n(lv, g.get_value(), rv)
                res.insert(0, TaggedValue(val, g.get_tag()))
            stack.append(val)
        # We get the top value of the accumulation
        return res

    def uacc_update(self, seg2, k, lc, rc):
        """
        Makes an update of the current accumulation, using initial values and the top accumulated values

        Parameters
        ----------
        seg :
            Result of a local accumulation
        k : lambda x,y,z -> r
            The function used to reduce a BTree into a single value
        lc :
            Top value of the left children in a global structure
        rc :
            Top value of the left children in a global structure

        Raises
        ------
        NotEqualSizeError:
            If the must be updated Segment and the pre-accumulated Segment does not have the same size
        IllFormedError:
            If the current instance does not represent a correct linearized subtree
            That is there is a node that doesn't have two children
        """

        if self.length() != seg2.length():
            raise NotEqualSizeError("uacc_update cannot needs to Segment of same size as input")

        stack = [rc, lc]
        d = MINUS_INFINITY
        res = Segment()
        for i in range(seg2.length() - 1, -1, -1):
            v1 = self[i]
            v2 = seg2[i]
            # We update the accumulation from seg2

            # We stack the values already updated to process updates on nodes

            if v1.is_leaf():
                # The result of the accumulation is the node made in seg2
                res.insert(0, v2)
                stack.append(v2.get_value())
                d = d + 1

            elif v1.is_node():
                if len(stack) < 2:
                    raise IllFormedError(
                        "uacc_update cannot be applied if there is a node that does not have two children in the current instance")
                # We need two sub accumulation values to process the accumulation of a node
                lv = stack.pop()
                rv = stack.pop()
                if d == 0 or d == 1:
                    # We met a critical value before, so the accumulation is not completed yet
                    val = k(lv, v1.get_value(), rv)
                    res.insert(0, TaggedValue(val, v1.get_tag()))
                    stack.append(val)
                    d = 0
                else:
                    # We did not meet a critical value before, so the accumulation is completed yet
                    res.insert(0, v2)
                    stack.append(v2.get_value())
                    d = d - 1
            else:  # v1.is_critical()
                if len(stack) < 2:
                    raise IllFormedError(
                        "uacc_update cannot be applied if there is a node that does not have two children in the current instance")
                # We need two sub accumulation values to process the accumulation of a critical node
                lv = stack.pop()
                rv = stack.pop()
                val = k(lv, v1.get_value(), rv)
                res.insert(0, TaggedValue(val, v1.get_tag()))
                stack.append(val)
                d = 0
        return res

    def dacc_path(self, phi_l, phi_r, psi_u):
        """
        Finds the critical node and then computes two values only on the path from the root node to the critical node

        Parameters
        ----------
        phi_l : lambda x -> y
            A function used to respect the closure property to allow partial computation on the left
        phi_r : lambda x -> y
            A function used to respect the closure property to allow partial computation on the right
        psi_u : lambda x,y,z -> r
            A function used to respect the closure property to make partial computation

        Raises
        ------
        EmptyError:
            If the methods is applied to an empty Segment
        ApplicationError:
            If the current instance does not contain a critical value
        """

        if self.is_empty():
            raise EmptyError("dacc_path cannot be applied to an empty Segment")
        d = MINUS_INFINITY
        # The value to pass to the left children for a total downward accumulation
        to_l = None
        # The value to pass to the right children for a total downward accumulation
        to_r = None
        has_critical = False
        for v in self.reverse():
            if v.is_leaf():
                d = d + 1
            elif v.is_node():
                if d == 0:
                    # The current node is an ancestor of a critical value by the left
                    # That is, there is a critical value on its left children in a BTree representation
                    # We process and stack the value of a partial downward accumulation
                    to_l = psi_u(phi_l(v.get_value()), to_l)
                    to_r = psi_u(phi_l(v.get_value()), to_r)
                elif d == 1:
                    # The current node is an ancestor of a critical value by the right
                    # That is, there is a critical value on its right children in a BTree representation
                    # We process and stack the value of a partial downward accumulation
                    to_l = psi_u(phi_l(v.get_value()), to_l)
                    to_r = psi_u(phi_l(v.get_value()), to_r)
                    d = 0
                else:
                    d = d - 1
            else:  # v.is_critical()
                has_critical = True
                to_l = phi_l(v.get_value())
                to_r = phi_r(v.get_value())
                d = 0
        if not has_critical:
            raise ApplicationError("dacc_path must be imperatively applied to a Segment which contains a critical node")
        return TaggedValue((to_l, to_r), "N")

    def dacc_global(self, psi_d, c):
        """
        Performs sequential downwards accumulation

        Parameters
        ----------
        psi_d :
            A function used to respect the closure property on gr and gl (initial functions used for upward accumulation) to make partial downward accumulation
        c :
            Initial value of the accumulator

        Raises
        ------
        ApplicationError:
            If the current instance contains a critical value
        IllFormedError:
            If the current instance does not represent a correct linearized subtree
            That is there are several leaves that doesn't have a parent in a BTree representation
        """

        stack = [c]
        res = Segment()
        if self.has_critical():
            raise ApplicationError("dacc_global cannot be applied to Segment which contains a critical node")
        for v in self:
            if len(stack) == 0:
                raise IllFormedError(
                    "dacc_global cannot be applied to ill-formed Segments that is two leaf values do not not have a parent")
            # We add the previous accumulation as a new value of our result
            val = stack.pop()
            res.append(TaggedValue(val, v.get_tag()))

            # If the current value is node, we need to update the value to pass to the right, and left children
            # These values are contained in the stack
            if v.is_node():
                (to_l, to_r) = v.get_value()
                stack.append(psi_d(val, to_r))
                stack.append(psi_d(val, to_l))
        return res

    def dacc_local(self, gl, gr, c):
        """
        Computes local downward accumulation for the current instance using an accumulative parameter resulting of a global downward accumulation

        Parameters
        ----------
        gl : lambda x,y -> z
            Function to make a downward accumulation to the left
        gr : lambda x,y -> z
            Function to make a downward accumulation to the right
        c :
            Initial value of the accumulator

        Raises
        ------
        IllFormedError:
            If the current instance does not represent a correct linearized subtree
            That is there are several leaves that doesn't have a parent in a BTree representation or if there is not a value to accumulate from above
        """

        # We update not finished accumulation locally using the value from the parent in the global representation of a linearized tree
        stack = [c]
        res = Segment()
        for v in self:
            if v.is_leaf() or v.is_critical():
                if len(stack) == 0:
                    raise IllFormedError(
                        "dacc_local cannot be applied if there are two leaf values, or critical values that do not have a parent")
                # We get the accumulated value passed from the last parent
                val = stack.pop()
                res.append(TaggedValue(val, v.get_tag()))
            else:  # v.is_node()
                if len(stack) == 0:
                    raise IllFormedError(
                        "dacc_local cannot be applied if there is not a value to accumulate from above")
                val = stack.pop()
                # We get the accumulated value passed from the last parent
                # And two new ones, one for the left children, and one to the right, using the gr and gl functions
                res.append(TaggedValue(val, v.get_tag()))
                stack.append(gr(val, v.get_value()))
                stack.append(gl(val, v.get_value()))
        return res

    def get_left(self, i):
        """
        Get the left children of a value at the i-th index

        Parameters
        ----------
        i :
            The index of the value that we want to get the left children

        Raises
        ------
        ApplicationError:
            Either if the current instance contains a critical error of is a leaf
        IllFormedError:
            There is no left children for the node at the i-th index in the current instance
        """
        if self.has_critical():
            raise ApplicationError("The left children of a value in a non-global Segment cannot be found")
        if self[i].is_leaf():
            raise ApplicationError("A leaf value doesn't have a left children")
        if i >= self.length() - 1:
            raise IllFormedError("Cannot get the left children of a node in an ill-formed Segment")
        return self[i + 1]

    def get_right(self, i):
        """
        Get the right children of a value at the i-th index

        Parameters
        ----------
        i :
            The index of the value that we want to get the right children

        Raises
        ------
        ApplicationError:
            Either if the current instance contains a critical error of is a leaf
        IllFormedError:
            There is no right children for the node at the i-th index in the current instance
        """
        if self.has_critical():
            raise ApplicationError("The right children of a value in a non-global Segment cannot be found")
        if self[i].is_leaf():
            raise ApplicationError("A leaf value doesn't have a right children")
        if i >= self.length() - 2:
            raise IllFormedError("Cannot get the left children of a node in an ill-formed Segment")

        def get_right_index(gt, i):
            if gt[i + 1].is_leaf():
                return i + 2
            else:
                return 1 + get_right_index(gt, i + 1)

        j = get_right_index(self, i)
        return self[j]

    def zip(self, seg):
        """
        Zip the values contained in a second Segment with the ones in the current instance

        Parameters
        ----------
        seg : Segment
            The Segment to zip with the current instance

        Raises
        ------
        NotEqualSizeError:
            If the size of seg is not the same one than the current instance or if two zipped segments doesn't have the same size
        NotSameTagError :
            If two values with not the same tag are trying to be zipped together
        """
        res = Segment()
        if self.length() != seg.length():
            raise NotEqualSizeError("The linearized trees have not the same shape")
        for j in range(self.length()):
            tv1 = self[j]
            tv2 = seg[j]
            if tv1.get_tag() != tv2.get_tag():
                raise NotSameTagError("Two zipped values have not the same tag")
            tv = TaggedValue((tv1.get_value(), tv2.get_value()), tv1.get_tag())
            res.append(tv)
        return res

    def map2(self, f, seg):
        """
        Zip the values contained in a second Segment with the ones in the current instance using a function

        Parameters
        ----------
        lt : Segment
            The Segment to zip with the current instance
        f : lambda x,y -> z
            A function to zip values

        Raises
        ------
        NotEqualSizeError:
            If the size of seg is not the same one than the current instance or if two zipped segments doesn't have the same size
        NotSameTagError :
            If two values with not the same tag are trying to be zipped together
        """
        res = Segment()
        if self.length() != seg.length():
            raise NotEqualSizeError("The linearized trees have not the same shape")
        for j in range(self.length()):
            tv1 = self[j]
            tv2 = seg[j]
            if tv1.get_tag() != tv2.get_tag():
                raise NotSameTagError("Two zipped values have not the same tag")
            tv = TaggedValue(f(tv1.get_value(), tv2.get_value()), tv1.get_tag())
            res.append(tv)
        return res


    def from_str(s, parser=int):
        """
        Get a segment from a string value

        Parameters
        ----------
        s : string
            The string to parse into a segment
        """
        res = Segment()
        s = s.replace(LEFT_SEG, "")
        s = s.replace(RIGHT_SEG, "")
        values = s.split(SEPARATOR_SEG)
        for v in values:
            v = v.replace(LEFT_TV, "")
            v = v.replace(RIGHT_TV, "")
            tv = v.split(SEPARATOR_TV)
            res.append(TaggedValue(parser(tv[0]), parseVTag(tv[1])))
        return res


# ------------------------------- #


class LTree(SList):
    """
    A list of Segment

    Methods
    -------
    init_from_bt(bt, m)
        Create a LTree from a BTree
    init_from_file(filename)
        Initialize a LTree from a file
    write_file(filename)
        Write a file that contains the current instance
    map(kl, kn)
        Applies function to every element of the current instance
    reduce(k, phi, psi_n, psi_l, psi_r)
        Makes a reduction of the current instance into a single value
    uacc(k, phi, psi_n, psi_l, psi_r)
        Processes an upward accumulation into the current instance
    dacc(gl, gr, c, phi_l, phi_r, psi_u, psi_d)
        Processes an downward accumulation into the current instance
    zip(lt)
        Zip the values contained in a second LTree with the ones in the current instance
    map2(lt, f)
        Zip the values contained in a second LTree with the ones in the current instance using a function
    deserialization()
        TODO
    """

    def __eq__(self, other):
        if isinstance(other, LTree):
            if self.length() != other.length():
                return False
            for i in range(0, self.length()):
                if self[i] != other[i]:
                    return False
            return True
        return False

    def __str__(self):
        res = ""
        for i in range(0, self.length()):
            res = res + str(self[i])
            if i != self.length() - 1:
                res = res + "\n"
        return res

    def init_from_bt(bt, m):
        """
        Create a LTree from a BTree

        Parameters
        ----------
        bt : BTree
            The BTree to transform into a LTree
        m : int
            Variable to define the critical nodes of bt
        """

        def __tv2lv(bt_val):
            val = bt_val.get_value()
            res = Segment()
            res_0 = Segment()
            if bt_val.is_leaf():
                res_0.append(val)
                res.append(res_0)
            else:  # bt_val.is_node()
                res_left = Segment(__tv2lv(bt_val.get_left()))
                res_right = Segment(__tv2lv(bt_val.get_right()))
                if val.is_critical():
                    res_0.append(val)
                    res.append(res_0)
                    res.extend(res_left)
                    res.extend(res_right)
                else:  # val.is_node()
                    res_0.append(val)
                    res_0.extend(res_left[0])
                    res_0.extend(res_right[0])
                    res.append(res_0)
                    res.extend(res_left[1:])
                    res.extend(res_right[1:])
            return res

        # Get a LTree from a BTree
        up_div = lambda n, m: (int(n / m) + (0 if n % m == 0 else 1))
        bt_one = bt.map(lambda x: 1, lambda x: 1)
        bt_size = bt_one.uacc(lambda x, y, z: x + y + z)
        bt_tags = bt_size.mapt(lambda x: VTag_LEAF,
                               lambda x, y, z: VTag_CRITICAL if up_div(x, m) > up_div(y.get_value(), m) and up_div(x,
                                                                                                                   m) > up_div(
                                   z.get_value(), m) else VTag_NODE)
        bt_val = bt.zipwith(lambda x, y: TaggedValue(x, y), bt_tags)
        return LTree(__tv2lv(bt_val))

    def init_from_file(filename, parser=int):
        """
        Initialize a LTree from a file

        Parameters
        ----------
        filename :
            The name of the file that contains the LTree to instantiate
        """
        if filename[-3:] != "." + EXT_FILE_LT:
            filename = filename + "." + EXT_FILE_LT
        res = LTree([])
        with open(filename, "r") as f:
            for line in f:
                a = Segment.from_str(line, parser=parser)
                res.append(a)
        f.close()
        return res

    def write_file(self, filename):
        """
        Write a file that contains the current instance

        Parameters
        ----------
        filename :
            The name of the file that we want to write the current instance in
        """
        if filename[-3:] != "." + EXT_FILE_LT:
            filename = filename + "." + EXT_FILE_LT
        with open(filename, "w+") as f:
            f.write(str(self))
        f.close()

    def map(self, kl, kn):
        """
        Applies function to every element of the current instance

        Parameters
        ----------
        kl : lambda x -> y
            Function to apply to every leaf value of the current instance
        kn : lambda x -> y
            Function to apply to every node value of the current instance

        Raises
        ------
        EmptyError:
            If the current instance is empty
        """
        if self.is_empty():
            raise EmptyError("map cannot be applied to an empty linearized tree")
        res = LTree()
        for seg in self:
            res.append(seg.map_local(kl, kn))
        return res

    def reduce(self, k, phi, psi_n, psi_l, psi_r):
        """
        Makes a reduction of the current instance into a single value

        The parameters must respect these equalities (closure property):
        * k(l, b, r) = psi_n(l, phi(b), r)
        * psi_n(psi_n(x, l, y), b, r) = psi_n(x, psi_l(l,b,r), y)
        * psi_n(l, b, psi_n(x, r, y)) = psi_n(x, psi_r(l,b,r), y)

        Parameters
        ----------
        k : lambda x,y,z -> r
            The function used to reduce a BTree into a single value
        phi : lambda x -> y
            A function used to respect the closure property to allow partial computation
        psi_n lambda x,y,z -> r
            A function used to respect the closure property to make partial computation
        psi_l : lambda x,y,z -> r
            A function used to respect the closure property to make partial computation on the left
        psi_r : lambda x,y,z -> r
            A function used to respect the closure property to make partial computation on the right

        Raises
        ------
        EmptyError:
            If the current instance is empty
        """

        if self.is_empty():
            raise EmptyError("reduce cannot be applied to an empty linearized tree")
        tops = Segment()

        # We start by doing local reductions on each Segment, representing a sub part of the tree
        for seg in self:
            tops.append(seg.reduce_local(k, phi, psi_l, psi_r))

        # The local reductions are reduced into a single value with reduce_global
        return tops.reduce_global(psi_n)

    def uacc(self, k, phi, psi_n, psi_l, psi_r):
        """
        Processes an upward accumulation into the current instance

        The parameters must respect these equalities (closure property):
        * k(l, b, r) = psi_n(l, phi(b), r)
        * psi_n(psi_n(x, l, y), b, r) = psi_n(x, psi_l(l,b,r), y)
        * psi_n(l, b, psi_n(x, r, y)) = psi_n(x, psi_r(l,b,r), y)

        Parameters
        ----------
        k : lambda x,y,z -> r
            The function used to reduce a BTree into a single value
        phi : lambda x -> y
            A function used to respect the closure property to allow partial computation
        psi_n lambda x,y,z -> r
            A function used to respect the closure property to make partial computation
        psi_l : lambda x,y,z -> r
            A function used to respect the closure property to make partial computation on the left
        psi_r : lambda x,y,z -> r
            A function used to respect the closure property to make partial computation on the right

        Raises
        ------
        EmptyError:
            If the current instance is empty
        """

        if self.is_empty():
            raise EmptyError("uacc cannot be applied to an empty linearized tree")
        gt = Segment()
        lt2 = LTree()
        # We first make a local accumulation to get
        # * Locally non complete accumulated segments
        # * The top value of accumulations, to later pass them for a complete accumulation
        for seg in self:
            (top, res) = seg.uacc_local(k, phi, psi_l, psi_r)
            gt.append(top)
            lt2.append(res)

        # We get real top values of accumulation considering a full linearized tree
        gt2 = gt.uacc_global(psi_n)

        res = LTree()

        # We update each segment using the real top values calculated previously,
        # the non complete accumulated segments and the initial segments
        for i in range(0, gt.length()):
            if gt[i].is_node():
                lc = gt2.get_left(i).get_value()
                rc = gt2.get_left(i).get_value()
                seg_res = self[i].uacc_update(lt2[i], k, lc, rc)
                res.append(seg_res)
            else:
                res.append(lt2[i])
        return res

    def dacc(self, gl, gr, c, phi_l, phi_r, psi_u, psi_d):
        """
        Processes an downward accumulation into the current instance

        The parameters must respect these equalities (closure property):
        * gl(c, b) = psi_d(c, phi_l(b))
        * gr(c, b) = psi_d(c, phi_r(b))
        * psi_d(psi_d(c, b), a) = psi_d(c, psi_u(b,a))

        Parameters
        ---------
        gl : lambda x,y,z -> r
            The function used to make an accumulation to the left children in a binary tree
        gr : lambda x,y,z -> r
            The function used to make an accumulation to the right children in a binary tree
        phi_l : lambda x -> y
            A function used to respect the closure property to allow partial computation on the left
        phi_r : lambda x -> y
            A function used to respect the closure property to allow partial computation on the right
        psi_d lambda x,y,z -> r
            A function used to respect the closure property to make partial downward accumulation
        psi_u : lambda x,y,z -> r
            A function used to respect the closure property to make partial computation

        Raises
        ------
        EmptyError:
            If the current instance is empty
        """

        if self.is_empty():
            raise EmptyError("dacc cannot be applied to an empty linearized tree")
        gt = Segment()
        res = LTree()
        # We first find the values to pass to sub trees for each segment that contains critical values
        # That is incomplete subtrees (which have node with left and right children not contained in the same segment)
        for seg in self:
            if seg.has_critical():
                gt.append(seg.dacc_path(phi_l, phi_r, psi_u))
            else:
                v = seg[0]
                gt.append(TaggedValue(v.get_value(), "L"))

        # We process a global downward accumulation using the initial value of the accumulator
        gt2 = gt.dacc_global(psi_d, c)

        # We finally pass the values of global accumulation to each segment, to update their local accumulation
        for i in range(0, gt.length()):
            res.append(self[i].dacc_local(gl, gr, gt2[i].get_value()))
        return res

    def zip(self, lt):
        """
        Zip the values contained in a second LTree with the ones in the current instance

        Parameters
        ----------
        lt : LTree
            The LTree to zip with the current instance

        Raises
        ------
        NotEqualSizeError:
            If the size of lt is not the same one than the current instance or if two zipped segments doesn't have the same size
        """
        res = LTree()
        if self.length() != lt.length():
            raise NotEqualSizeError("The linearized trees have not the same shape")
        for i in range(self.length()):
            res.append(self[i].zip(lt[i]))
        return res

    def map2(self, f, lt):
        """
        Zip the values contained in a second LTree with the ones in the current instance using a function

        Parameters
        ----------
        lt : LTree
            The LTree to zip with the current instance
        f : lambda x,y -> z
            A function to zip values

        Raises
        ------
        NotEqualSizeError:
            If the size of lt is not the same one than the current instance or if two zipped segments doesn't have the same size
        """
        res = LTree()
        if self.length() != lt.length():
            raise NotEqualSizeError("The linearized trees have not the same shape")
        for i in range(self.length()):
            res.append(self[i].map2(f, lt[i]))
        return res

    def deserialization(self):
        """
        TODO
        """

        def __graft(bt, lbt, rbt):
            val = bt.get_value()
            if bt.is_node():
                return Node(val, __graft(bt.get_left(), lbt, rbt), __graft(bt.get_right(), lbt, rbt))
            else:  # bt.is_leaf()
                return Node(val, lbt, rbt) if val.is_critical() else bt

        def __remove_annotation(bt):
            v = bt.get_value()
            return Leaf(v.get_value()) if bt.is_leaf() else Node(v.get_value(), __remove_annotation(bt.get_left()),
                                                                 __remove_annotation(bt.get_right()))

        def __lv2ibt(seg):
            stack = []
            has_crit = False
            if seg.is_empty():
                raise EmptyError("An empty Segment cannot be transformed into a BTree")
            for i in range(seg.length() - 1, -1, -1):
                v = seg[i]
                if v.is_leaf():
                    stack.append(Leaf(v))
                elif v.is_critical():
                    stack.append(Leaf(v))
                    if has_crit:
                        raise IllFormedError("A ill-formed Segment cannot be transformed into a BTree")
                    else:
                        has_crit = True
                else:
                    if len(stack) < 2:
                        raise IllFormedError("A ill-formed Segment cannot be transformed into a BTree")
                    lv = stack.pop()
                    rv = stack.pop()
                    stack.append(Node(v, lv, rv))
            if len(stack) != 1:
                raise IllFormedError("A ill-formed Segment cannot be transformed into a BTree")
            else:
                return (has_crit, stack[0])

        def __rev_segment_to_trees(lb, gt):
            stack = []
            for i in range(lb.length() - 1, -1, -1):
                if gt[i] == VTag_LEAF:
                    stack.append(lb[i])
                else:  # gt[i] == VTag_Node
                    lbt = stack.pop()
                    rbt = stack.pop()
                    stack.append(__graft(lb[i], lbt, rbt))
            if len(stack) != 1:
                raise IllFormedError("A ill-formed list of incomplete BTree cannot be transformed into a BTree")
            else:
                return stack[0]

        gt = SList()
        list_of_btree = SList()
        for seg in self:
            (has_crit, bt_i) = __lv2ibt(seg)
            list_of_btree.append(bt_i)
            if has_crit:
                gt.append(VTag_NODE)
            else:
                gt.append(VTag_LEAF)
        bt_annoted = __rev_segment_to_trees(list_of_btree, gt)
        return __remove_annotation(bt_annoted)
