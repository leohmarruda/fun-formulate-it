import utils
from operations import *
from inspect import signature
import itertools
import math
import re

def post_process_formula(s: str) -> str:
    s = re.sub(r'-1\*', '-', s)  # remove -1 multiplier
    s = re.sub(r'(^1\*|(?<=[^\d.])1\*)', '', s)  # remove 1 multiplier
    s = re.sub(r'\*1$', '', s)  # remove 1 multiplier
    s = re.sub(r'/1$', '', s)  # remove 1 divider
    s = re.sub(r'(\^1$|\^1(?=[^\d.]))', '', s)  # remove 1 exponent
    s = re.sub(r'(^1!|(?<=[^\d.])1!)', '', s)  # remove 1 factorial
    s = re.sub(r'\+-', '-', s)  # replace +- for -
    return s

def gen_terms(target: float, f_optional=True):
    """Finds the best term approximations using the given function list.
    Try all combinations for (-)a *a^b * a! *a /a and returns all the minimal difference ones.
    if f_optional, also tries not applying the function
    """
    funs = [negative, multiply_factorial, multiply_power, multiply, divide]

    args_list = []
    for f in funs:
        n_args = len(signature(f).parameters)
        nums = f.nums
        if n_args == 1:
            args = [None, []] if f_optional else [[]]
            args_list.append(args)
        elif n_args == 2:
            args = list(itertools.product(nums))
            if f_optional: args = [None] + args
            args_list.append(args)
        elif n_args == 3:
            args = list(itertools.product(nums, nums))
            if f_optional: args = [None] + args
            args_list.append(args)
    f_args = list(itertools.product(*args_list))  # all possible argument combinations

    min_res, abs_min_res, min_terms = float('inf'), float('inf'), []
    for c in f_args:
        result = 1
        formula = "1"
        for idx, f in enumerate(funs):
            arg = c[idx]
            if arg is not None:
                ans, s = f(result, *arg)
                result = ans
                formula = s.format(formula, *arg)
        if abs(target - result) < abs_min_res:
            min_res = target - result
            abs_min_res = abs(min_res)
            formula = post_process_formula(formula)
            min_terms = [(formula, min_res)]
        elif abs(target - result) == abs_min_res:
            min_res = target - result
            formula = post_process_formula(formula)
            if not (formula, min_res) in min_terms:
                min_terms.append((formula, min_res))
    return min_terms


def gen_factors(target: float, factors=3, precision=10):
    """Finds the best term approximations using the given function list.
    Try all combinations for +-a^b(c^d +- e^f) +- g^h and returns all the zero difference ones.
    TODO: try subtracting powers and trying again
    BUG: 31538859823 = 1543^4231(4831)
    """
    if target == 0: return 0
    if not math.isclose(target, round(target, 0)):
        target = round(target, precision)
        num, den = utils.irreducible_fraction(int(target * pow(10, precision)), int(pow(10, precision)))
        return [("{}/{}".format(gen_factors(num)[0][0], gen_factors(den)[0][0]), 0)]
    sign = 1 if target >= 0 else -1
    target /= sign

    fact_list = utils.get_factors(target)
    max_exp = max([x[1] for x in fact_list])
    max_common_factor, other_factors = [], []
    for x in fact_list:
        if x[1] == max_exp and max_exp > 1:
            max_common_factor.append(x)
        else:
            other_factors.append(x)
    if max_exp == 1:
        max_common_factor = other_factors[:-1]
        other_factors = [other_factors[-1]]
    terms = []
    if other_factors:
        f1 = utils.multiply_factors(other_factors)
        f1_strs = utils.find_difference_of_powers(f1) + [f1]
        for f1_str in f1_strs:
            formula = "{}({})".format(utils.factors_to_product_str(max_common_factor), f1_str)
            formula = post_process_formula(formula)
            terms.append([formula, 0])
    else:
        formula = "{}".format(utils.factors_to_product_str(max_common_factor))
        formula = post_process_formula(formula)
        terms.append([formula, 0])
    return terms
