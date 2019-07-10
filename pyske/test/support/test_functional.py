from pyske.core.support.functional import *


def test_composition():
    f = lambda x: x + 1
    g = lambda x: x - 9
    x = 0
    fcts = [f, g]
    c = Composition(*fcts)
    res = c(x)
    exp = f(g(x))

    assert res == exp
