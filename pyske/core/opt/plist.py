from pyske.core.opt.term import modules, Term
from pyske.core.opt.rules import inner_most_strategy
import importlib

module_name = 'PList'
module_pyske = 'pyske.core.list.plist'
modules.update({module_name: importlib.import_module(module_pyske)})

class PList(Term):

    def __init__(self, f='__init__', a=['PList'], s=True):
        self.static = s
        self.function = f
        self.arguments = a

    @staticmethod
    def init(f, size):
        return PList('init', ['PList', f, size])

    def run(self):
        opt = inner_most_strategy(self)
        return opt.eval()

    def __getattr__(self, item):
        def f(*args):
            return PList(item, [self] + list(args), False)
        return f