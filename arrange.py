from __future__ import print_function, division, unicode_literals
from six.moves import zip
from itertools import permutations, combinations, product, takewhile, starmap
from blist import sortedlist
from io import open


def arrangements(lines, n=2):
    """Yield every possible arrangement of lines.

    Considers merging two lines when the last n characters of a line equal
    the first n characters of another. Lines are sorted."""
    try:
        lines = sortedlist(lines)
        for pairs in pairings(*overlapping(lines, n)):
            copy = sortedlist(lines)
            for left, right in pairs:
                copy.remove(left)
                copy.remove(right)
                copy.add(left + right[n:])
            for solution in arrangements(copy):
                yield solution
    except NoOverlap:
        yield lines
        return


def overlapping(lines, n=2):
    """Find lines that could overlap.

    Returns two lists: all lines that share a suffix and all lines that use
    the same string as their prefix. Raises NoOverlap if none found."""
    lines = sortedlist(lines)
    for left in lines:
        overlap = left[-n:]
        rights = list(takewhile(
            lambda right: right.startswith(overlap),
            lines[lines.bisect_left(overlap):]))
        if left in rights:
            rights.remove(left)
        if rights:
            lefts = [l for l in lines if l.endswith(overlap)]
            return (lefts, rights)
    raise NoOverlap()


class NoOverlap(ValueError):
    pass


def pairings(lefts, rights):
    """Yield every possible pairing of strings from two sorted lists."""
    n = min(len(lefts), len(rights))
    return starmap(zip, product(
        combinations(lefts, n),
        permutations(rights, n)))


def variance(samples):
    avg = sum(samples) / len(samples)
    return sum(map(lambda l: (len(l) - avg) ** 2,
                   solution)) / len(solution)


if __name__ == "__main__":
    with open("cartouches.txt", encoding="utf-8") as f:
        cartouches = f.read().splitlines()
    solutions = arrangements(cartouches)
    for solution in solutions:
        print(variance(list(map(len, solution))), " ".join(solution))
