from pyske.core.runnable.rule.rule_slist import *
from pyske.core.runnable.rule.rule_plist import *
from pyske.core.runnable.transformation import transformation

rules = rules_slist + rules_plist

def run(t, rules = rules):
    t = transformation(t, rules)
    return t.run()
