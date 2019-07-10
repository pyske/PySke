class Composition:

    def __init__(self, *fcts):
        if isinstance(fcts, list):
            fcts = tuple(fcts)

        self.fcts = fcts

    def __call__(self, arg):
        res = arg
        for f in self.fcts:
            res = f(res)
        return res
