from __future__ import print_function
from multiprocessing import Pool
from itertools import permutations
from functools import partial
import re

alphabet = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
likely_substitutions = {
    "A": "FYGPBVKXJQZ",
    "B": "AOI",
    "C": "INSHRDL",
    "D": "NSHRDLU",
    "G": "ETAO",
    "H": "UCMWFY",
    "I": "UCMWFY",
    "J": "FYGPBVKXJQZ",
    "K": "INSHRDL",
    "L": "UCMWFY",
    "M": "CMWFYGPB",
    "O": "INSHRDL",
    "Q": "ETA",
    "R": "FYGPBVKXJQZ",
    "T": "NSHRDLU",
    "U": "OINSH",
    "V": "ETA",
    "W": "CMWFYGPB",
    "X": "NSHRDLU",
    "Z": "RDLUCMW"}


def inv_index_iter(ciphertext_symbols):
    """Yield every likely substitution cipher for a short ciphertext."""
    if not ciphertext_symbols:
        yield {}
        return
    remaining = ciphertext_symbols.copy()
    symbol = remaining.pop()
    for cipher in inv_index_iter(remaining):
        for substitution in likely_substitutions[symbol]:
            cipher[symbol] = substitution
            yield cipher.copy()


def ciphertext_alphabet(inv_index, plaintext_alphabet=alphabet):
    """Compute the full ciphertext alphabet from a partial inverse mapping."""
    index = {v: k for k, v in inv_index.items()}
    return [index.get(s, '_') for s in alphabet]


def words(min_len, max_len, alphabet=alphabet):
    with open("words.txt") as f:
        for w in f.read().splitlines():
            w = w.upper()
            if min_len < len(w) < max_len and set(w).issubset(alphabet):
                yield w


def brute_force(ciphertext):
    results = []
    for inv_index in inv_index_iter(set(ciphertext)):
        plaintext = "".join(inv_index[c] for c in ciphertext)
        matches = word_regex.findall(plaintext)
        if matches and sum(map(len, matches)) > 5:
            results.append(["".join(ciphertext_alphabet(inv_index)),
                "".join(ciphertext), plaintext] + matches)
    return results


def ciphertext_iter():
    with open("ciphertext.txt") as f:
        ciphertexts = f.read().splitlines()
    for row in ciphertexts:
        for perm in permutations(row):
            yield perm
    for y in range(min(map(len, ciphertexts))):
        col = [ciphertexts[y][x] for x in range(len(ciphertexts))]
        yield col
        yield list(reversed(col))


word_regex = re.compile("|".join(set(map(re.escape, words(3, 10)))))

if __name__ == "__main__":
    for results in Pool(8).imap_unordered(brute_force, ciphertext_iter()):
        for match in results:
            print(" ".join(match))
