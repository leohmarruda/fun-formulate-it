from collections import Counter
import math


def check_res_signs(lst):
    return next((x for x in lst if x > 0), 0), next((x for x in lst if x < 0), 0)


def irreducible_fraction(numerator, denominator):
    divisor = math.gcd(numerator, denominator)
    return numerator // divisor, denominator // divisor


def factors_to_product_str(tuple_list):
    return '*'.join([f"{a}^{b}" for a, b in tuple_list])


def get_factors(n):
    return list(Counter(factorize(n)).items())


def multiply_factors(factors: list):
    p = 1
    for f in factors:
        p *= pow(f[0], f[1])
    return p


def factorize(n):
    sieve = [True] * int(n ** 0.5 + 2)
    for x in range(2, int(len(sieve) ** 0.5 + 2)):
        if not sieve[x]:
            continue
        for i in range(x * x, len(sieve), x):
            sieve[i] = False
    factors = []
    for i in range(2, len(sieve)):
        if i * i > n:
            break
        if not sieve[i]:
            continue
        while n % i == 0:
            factors.append(int(i))
            n //= i
    if n > 1:
        factors.append(int(n))
    return factors


def find_difference_of_powers(n, max_base=10, max_power=10):
    diff_str = []
    for a in range(1, max_base + 1):
        for b in range(1, max_base + 1):
            for x in range(1, max_power + 1):
                for y in range(1, max_power + 1):
                    if a**x - b**y == n:
                        diff_str.append("{}^{}-{}^{}".format(a,x,b,y))
                    break
    return diff_str