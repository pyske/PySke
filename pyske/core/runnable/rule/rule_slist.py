from pyske.core.runnable.list.slist import SList
from pyske.core.runnable.transformation import *
from pyske.core.support.functional import *
from pyske.core.runnable.rule.rule import *

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

map_composition_rule = Rule(left1, right1)

# -----------------------------

rules_slist = [map_reduce_rule, map_composition_rule]