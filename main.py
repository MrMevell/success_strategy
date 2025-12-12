import random
from functools import lru_cache


# Вычисление факториалов до n включительно
def factorial(n):
    array = [1] * (n + 1)
    for i in range(2, n + 1):
        array[i] = i * array[i - 1]
    return array


@lru_cache
# @skip - число пропущенных билетов
# @n    - число билетов
def probability_for_max(skip, n):
    if skip == 1:    # если skip равен 1, то мы пропускаем
        return 1 / n # skip - 1 = 0 билетов

    probability = 0
    for k in range(skip - 1, n):
        probability += 1 / k
    return (skip - 1) / n * probability


@lru_cache
# @n - число билетов
def skip_for_max(n):
    for skip in range(1, n):
        if(skip / n) > probability_for_max(skip+1, n):
            return skip
    return 1 # возвращается, если при s > 1 не выполняется условие выше


@lru_cache
# @skip - число пропущенных билетов
# @n    - число билетов
def average(skip, n):
    factorials = factorial(n)

    if skip == 1:
        result = 0
        for k in range(1, n + 1):
            result += k
        return result / n

    result = 0
    for k in range(skip, n+1):
        current = 0
        for i in range(skip-1, k):
            current += (factorials[k-1] * (skip - 1) * factorials[n - i - 1]
                        / (i * factorials[k - i - 1] * factorials[n]))
        result += k * current
    return result


@lru_cache
# @n - число билетов
def skip_for_aver(n):
    last = 0
    current = average(1, n)
    for skip in range(1, n):
        next = average(skip + 1, n)

        if current > last and current > next:
            return skip

        last = current
        current = next
    return 1


# @n      - число билетов
# @repeat - число повторов
def modeling(n, repeat):

    print(f"{'n':<8}{'s(π)':<20}{'π(s, n)':<20}{'sim π':<20}{'Δπ':<20}"
          f"{'s(Mξ)':<20}{'Mξ(s, n)':<20}{'sim Mξ':<20}{'ΔMξ':<20}")
    print("=" * 160)

    for ticket in range(1, n+1):
        total_max = 0
        total_aver = 0

        # Оптимальные пробные серии
        correct_max = skip_for_max(ticket)
        correct_aver = skip_for_aver(ticket)

        skip_max = skip_for_aver(ticket)
        skip_aver = skip_for_max(ticket)

        # Оптимальные результаты
        opt_max = round(probability_for_max(correct_max, ticket), 5)
        opt_aver = round(average(correct_aver, ticket), 5)

        arr = list(range(1, ticket+1))
        for _ in range(repeat):
            random.shuffle(arr)

            # Средний выигрыш
            if skip_aver == 1:
                total_aver += arr[0]
            else:
                max_trial = max(arr[:skip_aver-1])
                for value in arr[skip_aver-1:]:
                    if value > max_trial:
                        total_aver += value
                        break

            # Максимальный выигрыш
            if skip_max == 1:
                max_trial = 0
            else:
                max_trial = max(arr[:skip_max-1])
            first_max = None
            for value in arr[skip_max-1:]:
                if value > max_trial:
                    first_max = value
                    break
            if first_max == max(arr):
                total_max += 1

        # Результаты
        prob_max = round(total_max / repeat, 5)
        aver = round(total_aver / repeat, 5)

        # Разница
        diff_max = round(abs(prob_max - opt_max), 5)
        diff_aver = round(abs(aver - opt_aver), 5)

        print(f"{ticket:<8}{correct_max:<20}{opt_max:<20}{prob_max:<20}{diff_max:<20}"
                f"{correct_aver:<20}{opt_aver:<20}{aver:<20}{diff_aver:<20}")


def table(n):
    print(f"{'n':<8}{'s(π)':<20}{'π(s, n)':<20}"
          f"{'s(Mξ)':<20}{'Mξ(s, n)':<20}")
    print("=" * 88)

    for ticket in range(1, n + 1):
        skip_max = skip_for_max(ticket)
        skip_aver = skip_for_aver(ticket)

        prob_max = probability_for_max(skip_max, ticket)
        aver = average(skip_aver, ticket)

        print(f"{ticket:<8}{skip_max:<20}{round(prob_max, 10):<20}{skip_aver:<20}{round(aver, 10):<20}")


n = int(input("Введите количество билетов: "))
modeling(n, 10**7)
table(n)