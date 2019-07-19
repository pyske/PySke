import functools
import types
from functools import reduce
from pyske.core.opt.util import merge

modules = {}


class Var(str):
    pass


class Term:

    def __init__(self, f, a, s=False):
        self.static = s
        self.function = f
        self.arguments = a
        
    def eval(self):
        vargs = [e.eval() if issubclass(type(e), Term) else e for e in self.arguments]
        if isinstance(self.function, (types.FunctionType, types.BuiltinFunctionType, functools.partial)):
            return self.function(*vargs)
        if self.function == "__raw__":
            return self.arguments[0]
        # arguments is assumed to be non-empty: it is either the class or object
        # to which the function/method is applied
        cn = vargs.pop(0)
        # Getting the class or object
        if self.static:
            co = getattr(modules[cn], cn)
        else:
            co = cn
        if self.function == '__init__':
            return co(*vargs)
        else:
            return getattr(co, self.function)(*vargs)

    def graft(self, pos, t):
        i = pos.pop(0)
        if pos == []:
            self.arguments[i] = t
        else:
            self.arguments[i].graft(pos, t)


    def __match(obj, pattern):
        if type(pattern) is Var:
            return { pattern: obj }
        if isinstance(obj, Term):
            return obj.match(pattern)
        if obj == pattern:
            return {}
        return None
            

    def match(self, pattern):
        if type(pattern) is Var:
            subst = {pattern: self}
        elif isinstance(pattern, Term) and self.function == pattern.function \
                and len(self.arguments) == len(pattern.arguments):
            ss = [Term.__match(self.arguments[i], pattern.arguments[i])
                  for i in range(0, len(self.arguments))]
            subst = reduce(merge, ss)
        else:
            subst = None
        return subst
            

    def __str__(self):
        if self.function == "__raw__":
            return "RAW("+str(type(self.arguments[0]))+")"
        else:
            return ("[static]" if self.static else "")+str(self.function) +\
                   "(" + reduce(lambda x, y: x + ", " + y, map(str, self.arguments)) + ")"
        # return str(self.arguments[0])+"."+self.function+"("+\
        #        reduce(lambda x, y: x+", "+y, map(str, self.arguments[1:]))+")"



def subst(t, s):
    if isinstance(t, Var) and t in s:
        return s[t]
    elif isinstance(t, Term):
        return Term(t.function,
                    [subst(e, s) for e in t.arguments],
                    t.static)
    return t
