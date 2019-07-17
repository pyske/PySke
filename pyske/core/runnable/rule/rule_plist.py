from pyske.core.runnable.list.plist import PList
from pyske.core.list.plist import PList as Core_PList

from pyske.core.runnable.transformation import *
from pyske.core.support.functional import *
from pyske.core.runnable.rule.rule import *

left0 = PList(PList.__name__, [PList(PList.__name__, [tag_VAR_pattern, Core_PList.map.__name__, tag_VAR_pattern]),
                               Core_PList.reduce.__name__,
                               tag_VAR_pattern,
                               tag_VAR_pattern]
              )
right0 = PList(PList.__name__, [Position([0, 0, 0]), Core_PList.map_reduce.__name__, Position([0, 0, 2]), Position([0, 2]), Position([0, 3])])

map_reduce_rule = Rule(left0, right0)

# -----------------------------

left1 = PList(PList.__name__,   [PList(PList.__name__, [tag_VAR_pattern,  Core_PList.map.__name__, tag_VAR_pattern]),
                                 Core_PList.map.__name__, tag_VAR_pattern]
             )

right1 = PList(PList.__name__, [Position([0, 0, 0]), Core_PList.map.__name__, Composition(Position([0, 2]),
                                                                                          Position([0, 0, 2]))
                                ])

map_composition_rule = Rule(left1, right1)

# -----------------------------

rules_plist = [map_reduce_rule, map_composition_rule]