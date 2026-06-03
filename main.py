from functools import lru_cache
import math

def probability_of_max(s, n):
    if s == 1:
        return 1.0 / n
    harmonic_sum = sum(1.0 / k for k in range(s - 1, n))
    return (s - 1) * harmonic_sum / n


def optimal_s_probability(n):
    for s in range(1, n):
        if (s / n) > probability_of_max(s + 1, n):
            return s
    return 1

@lru_cache
def average(s, n):
    if s == 1:
        return (n + 1) / 2.0

    result = 0.0
    ln_n_fact = math.lgamma(n + 1)  # ln(n!)

    for k in range(s, n + 1):
        ln_k_fact = math.lgamma(k + 1)  # ln(k!)
        current = 0.0
        for i in range(s, k + 1):
            # Считаем члены через логарифмы, чтобы избежать переполнения float при n >= 171
            ln_term = (ln_k_fact + math.lgamma(n - i + 1)
                       - ln_n_fact - math.lgamma(k - i + 1)
                       - math.log(i - 1))
            current += math.exp(ln_term)
        result += current

    return (s - 1) * result


def optimal_s_average(n):
    if average(1, n) >= average(2, n):
        return 1
    if average(n, n) >= average(n - 1, n):
        return n
    for s in range(2, n):
        val = average(s, n)
        if val > average(s - 1, n) and val >= average(s + 1, n):
            return s
    return 1


def solve_inequality(n, c):
    s_min, s_max = None, None
    for s in range(1, n + 1):
        if average(s, n) >= c:
            s_min = s
            break
    for s in range(n, 0, -1):
        if average(s, n) >= c:
            s_max = s
            break
    return s_min, s_max


def optimal_s_constrained(n, c):
    s_star = optimal_s_probability(n)
    s_min, s_max = solve_inequality(n, c)
    if s_min is None:
        return None
    if s_star < s_min:
        return s_min
    elif s_star > s_max:
        return s_max
    else:
        return s_star


n = int(input("Введите количество билетов: "))

print(f"Оптимальное s для вероятности: {optimal_s_probability(n)}")
print(f"Оптимальное s для матожидания: {optimal_s_average(n)}")

c = float(input("Введите ограничение c: "))
s_prime, s_double_prime = solve_inequality(n, c)

if s_prime is not None:
    print(f"Допустимый интервал A: [{s_prime}, {s_double_prime}]")
    s_tilde = optimal_s_constrained(n, c)
    print(f"Компромиссное s~: {s_tilde}")
    print(f"Итоговая вероятность pi({s_tilde}, {n}): {probability_of_max(s_tilde, n):.4f}")
    print(f"Итоговое матожидание M[xi({s_tilde})]: {average(s_tilde, n):.4f}")
else:
    print("Допустимых решений нет (C слишком велико)")