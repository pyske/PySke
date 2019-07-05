from abc import ABC, abstractmethod
from pyske.core.tree.rtree import RNode

import hashlib

ID_var = hashlib.md5(b'var')


class ETree (ABC, RNode):

    @abstractmethod
    def run(self):
        pass
