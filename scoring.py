import math
import re

def length_score(formula: str) -> float:
    return 1 / len(formula)

def palinseq_score(formula: str) -> float:
    """Parse all numbers, score each once"""
    def palin_score(n_str: str):
        score = -1
        for idx, el in enumerate(n_str):
            if n_str[idx] == n_str[-idx-1]: score += 1
            if idx > len(n_str) / 2: break
        return score

    def seq_score(n_str: str):
        if len(n_str) < 2: return 0
        score = 0
        for idx in range(len(n_str)-1):
            if int(n_str[idx]) - int(n_str[idx+1]) == 1:
                score += 1
            else:
                score = 0
                break
        if not score:
            for idx in range(len(n_str)-1):
                if int(n_str[idx]) - int(n_str[idx+1]) == -1:
                    score += 1
                else:
                    score = 0
                    break
        return score

    nums = re.findall(r'\d+', formula)
    score = 0
    for idx, num in enumerate(nums):
        score += max(palin_score(num), seq_score(num))
    return score / math.sqrt(len(formula))

def high_score(formula: str) -> float:
    score = 0
    facts = re.findall(r'\d+(?=!)', formula)
    exps = re.findall(r'(?<=\^)\d+', formula)
    n_divs = formula.count('/')
    for n in facts:
        if int(n) > 2: score += (int(n)-2)^2
    for n in exps:
        if int(n) > 2: score += 2*(int(n)-2)
    score -= n_divs
    return score / math.sqrt(len(formula))


def palinseqhigh_score(formula: str) -> float:
    return palinseq_score(formula) + high_score(formula)
