def merge(d1: dict, d2: dict):
    if d1 is None or d2 is None:
        return None
    keys1 = d1.keys()
    keys2 = d2.keys()
    if not(keys1 & keys2 == set()):
        raise Exception("Non linear patterns not supported")
    d = { k: d1[k] for k in keys1}
    d.update({ k: d2[k] for k in keys2})
    return d




