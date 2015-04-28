from __future__ import print_function
from __future__ import division
from blist import sortedlist, sortedset


def arrangements(lines):
    """Yield every possible arrangement of lines.

    Considers merging two lines when the last two characters of a line equal
    the first two characters of another. The lines in an arrangement are
    sorted. Solutions do repeat if they contain repated bigraphs.
    """
    lines = sortedlist(lines)

    # Find one available overlap and fixate on it.
    for i in range(len(lines)):
        left = lines[i]
        overlap = left[-2:]
        start = end = lines.bisect_left(overlap)
        while end < len(lines) and overlap == lines[end][:2]:
            end += 1
        # Ignore this overlap if one line only matches itself.
        if end > start + 1 or (end > start and not start <= i < end):
            break
        overlap = None

    # No lines paired. End recursion and emit solution.
    if not overlap:
        yield lines
        return

    # Recursively try each pair.
    for left in lines:
        if left[-2:] != overlap:
            continue
        for right in lines[start:end]:
            copy = sortedlist(lines)
            copy.remove(right)
            try:
                copy.remove(left)
            except ValueError:
                continue
            copy.add(left + right[2:])
            for solution in arrangements(copy):
                yield solution


def with_variance(solutions):
    for solution in solutions:
        avg = sum(map(len, solution)) / len(solution)
        variance = sum(map(lambda l: (len(l) - avg) ** 2,
            solution)) / len(solution)
        yield [variance] + list(solution)


if __name__ == "__main__":
    with open("cartouches.txt") as f:
        cartouches = f.read().splitlines()
    solutions = arrangements(cartouches)
    for solution in sortedset(with_variance(solutions))[:20]:
        print(" ".join(map(str, solution)))
