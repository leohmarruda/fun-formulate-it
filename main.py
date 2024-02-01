"""
FORMULATE-IT
This app generates a list of formulas approximating a given number and then ranks them based on "interestingness".

TODO: gen_factor has some calculation bug, needs to be refactored and improved.
"""
import utils
from generator import *
import scoring
import itertools
from math import isclose
import sys


def gen_approximations(target: float, max_terms: int = 2, max_n: int = 100) -> list:
    """Generates a list of approximations for the target number.
    Tries to approximate using the first term, then repeats for the residues.
    Return: list of pairs (formula string, residue)"""

    term_options = []
    positive_res, negative_res = utils.check_res_signs([target])
    for t in range(max_terms):
        new_terms = []
        if positive_res:
            new_terms += gen_terms(positive_res)
        if negative_res:
            new_terms += gen_terms(negative_res)
        if new_terms: term_options.append(new_terms)
        positive_res, negative_res = utils.check_res_signs([x[1] for x in new_terms])

    # generates all possible term combinations
    combinations = list(itertools.product(*term_options))
    gens = []
    for c in combinations:
        formula = "+".join([t[0] for t in c])
        formula = post_process_formula(formula)
        res = c[-1][1]
        if isclose(res, round(res, 0)): res = round(res, 0)  # rounds if integer
        if res != 0: formula += " res:" + str(res)
        gens.append(formula)
    gens = [x[0] for x in gen_factors(target)] + gens
    return gens[:max_n]


def score(formula: str, method="palinseqhigh") -> int:
    methods = {
        "length": scoring.length_score,
        "palinseq": scoring.palinseq_score,
        "high": scoring.high_score,
        "palinseqhigh": scoring.palinseqhigh_score
    }
    return methods[method](formula)


def rank(candidates):
    candidates.sort(key=score, reverse=True)
    return candidates


def print_results(target, candidates):
    print("target:", target)
    for n, c in enumerate(candidates):
        print(n + 1, c)


def main(argv, argc):
    target = 31538859823
    max_n = 100
    if len(argv) > 1:
        try:
            target = float(argv[1])
            if len(argv) > 2:
                max_n = float(argv[2])
        except ValueError:
            print("Number argument invalid, using default value")
    print_results(target, rank(gen_approximations(target, max_terms=4, max_n=max_n)))


if __name__ == '__main__':
    main(sys.argv, len(sys.argv))
