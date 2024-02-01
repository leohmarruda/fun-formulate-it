"""Repository of operations and functions to be used in the formulas."""
import math


def multiply_power(x: float, a: float, b: float) -> (float, str):
    return x * pow(a, b), '{}*{}^{}'
multiply_power.nums = [2, 3, 4, 5, 6, 7, 8, 9, 10]


def divide(x: float, a: float) -> (float, str):
    return x / a, '{}/{}'
divide.nums = [2, 3, 4, 5, 6, 7, 8, 9, 10, 12]


def multiply(x: float, a: float) -> (float, str):
    return x * a, '{}*{}'
multiply.nums = [2, 3, 4, 5, 6, 7, 8, 9, 10]

def multiply_factorial(x: float, a: int) -> (int, str):
    return x*math.factorial(a), "{}*{}!"
multiply_factorial.nums = [3, 4, 5, 6, 7, 8, 9, 10]


def negative(x: float) -> (float, str):
    return -x, '-{}'
negative.nums = []
