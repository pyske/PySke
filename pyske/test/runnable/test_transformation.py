from pyske.core.runnable.list.slist import SList
from pyske.core.runnable.transformation import *
from pyske.core.support.functional import *

# -----------------------------

class ETree_concrete(ETree):

    def __init__(self, v, ts=None):
        self.value = v
        if ts is None:
            self.children = Core_SList([])
        else:
            self.children = Core_SList(ts)

    def run(self):
        pass


# -----------------------------
precision_float = 0.00000001
# -----------------------------

left0 = SList(SList.__name__, [SList(SList.__name__, [tag_VAR_pattern, Core_SList.map.__name__, tag_VAR_pattern]),
                               Core_SList.reduce.__name__,
                               tag_VAR_pattern,
                               tag_VAR_pattern]
              )
right0 = SList(SList.__name__, [Position([0, 0, 0]), Core_SList.map_reduce.__name__, Position([0, 0, 2]), Position([0, 2]), Position([0, 3])])

map_reduce_rule = Rule(left0, right0)

# -----------------------------

left1 = SList(SList.__name__,   [SList(SList.__name__, [tag_VAR_pattern,  Core_SList.map.__name__, tag_VAR_pattern]),
                                 Core_SList.map.__name__, tag_VAR_pattern]
             )

right1 = SList(SList.__name__, [Position([0, 0, 0]), Core_SList.map.__name__, Composition(Position([0, 2]),
                                                                                          Position([0, 0, 2]))
                                ])

map_composition = Rule(left1, right1)

# -----------------------------

rules = [map_reduce_rule]

# -----------------------------

def test_matching_correct_simpl():
    f = lambda x: x
    op = lambda x, y: x+y
    cs = SList([1,2,3])
    tree = cs.map(f).reduce(op)
    assert matching(tree, left0)


def test_matching_correct_elaborate():
    f = lambda x: x
    op = lambda x, y: x+y
    ops = lambda x, y: x-y
    cs = SList([1,2,3])
    tree = cs.scan(ops, 0).map(f).reduce(op)
    assert matching(tree, left0)


def test_matching_incomplete_red():
    op = lambda x, y: x+y
    cs = SList([1, 2, 3])
    tree = cs.reduce(op)
    assert not matching(tree, left0)


def test_matching_incomplete_map():
    f = lambda x: x
    cs = SList([1,2,3])
    tree = cs.map(f)
    assert not matching(tree, left0)


def test_matching_incorrect():
    ops = lambda x, y: x-y
    cs = SList([1,2,3])
    tree = cs.scan(ops, 0)
    assert not matching(tree, left0)

# -----------------------------


def test_get_elem_etree_position_ok():
    exp = 'E'
    t = ETree_concrete('A',
                   [ETree_concrete('B'),
                    ETree_concrete('C',
                                   [exp,
                                    'F']),
                    ETree_concrete('D')
                    ]
                   )
    res = get_elem_etree_position(t, Position([0, 1, 0]))
    assert exp == res


def test_get_elem_etree_position_ko():
    exp = 'E'
    t = ETree_concrete('A',
                   [ETree_concrete('B'),
                    ETree_concrete('C',
                                   ['E',
                                    'F']),
                    ETree_concrete('D')
                    ]
                   )
    res = get_elem_etree_position(t, Position([0, 1, 1]))
    assert not exp == res

# -----------------------------

def test_rewrite_map_reduce():
    f = lambda x: x
    op = lambda x, y: x+y
    e = 0
    cs = SList([1, 2, 3])
    tree = cs.map(f).reduce(op, e)
    exp = cs.map_reduce(f, op, e)
    res = rewrite(tree, right0)
    assert exp == res


def test_rewrite_map_reduce_adv():
    f = lambda x: x
    op = lambda x, y: x+y
    ops = lambda x, y: x-y
    e = 0
    c = 0
    cs = SList([1, 2, 3])
    tree = cs.scan(ops, c).map(f).reduce(op, e)
    exp = cs.scan(ops, c).map_reduce(f, op, e)
    res = rewrite(tree, right0)
    assert exp == res



def test_map_compo():
    f = lambda x: x * 0.9
    g = lambda x: x * 1.1
    cs = SList([1, 2, 3])
    tree = cs.map(f).map(g)
    exp = cs.map(Composition(f, g)).run()
    res = rewrite(tree, right1).run()
    for i in range(len(exp)):
        assert (exp[i] - res[i]) <= precision_float

# -----------------------------

def test_one_transformation():
    f = lambda x: x
    op = lambda x, y: x+y
    e = 0
    cs = SList([1, 2, 3])
    tree = cs.map(f).reduce(op, e)
    exp = cs.map_reduce(f, op, e)
    rules = [map_reduce_rule]
    res = transformation(tree, rules)
    assert exp == res


def test_double_transformation():
    f = lambda x: x
    op = lambda x, y: x+y
    e = 0
    cs = SList([1, 2, 3])

    tree = cs.map(f).reduce(op, e).map(f).reduce(op, e)

    exp = cs.map_reduce(f, op, e).map_reduce(f, op, e)

    res = transformation(tree, rules)
    assert exp == res
