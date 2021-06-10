import random


# ------- Maximum Segment Sum -------


def list_to_segment(list):
    res = []
    for i in range(0, len(list)):
        for j in range(i + 1, len(list) + 1):
            res.append(list[i:j])
    return res


# ------- Maximum Segment Sum (two-dimensional lists)-------


def is_matrix(list):
    length = len(list[0])
    for elem in list:
        if len(elem) != length:
            return False
    return True


def list_2d_to_segment(list):
    assert is_matrix(list)
    largeur = len(list)
    hauteur = len(list[0])
    res = []
    for j in range(0, largeur):
        for k in range(0, hauteur):
            for x in range(0, largeur):
                for y in range(0, hauteur):
                    sousliste = []
                    for a in range(j, largeur - x):
                        for b in range(k, hauteur - y):
                            sousliste.append(list[a][b])
                    if sousliste:
                        res.append(sousliste)
    return res


# ------- Maximum Prefix Sum -------


def list_to_prefix(list):
    res = []
    for i in range(1, len(list) + 1):
        res.append(list[:i])
    return res


def frdm():
    return random.randint(-99, 99)