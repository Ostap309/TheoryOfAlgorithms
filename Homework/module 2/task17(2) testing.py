from itertools import permutations
import numpy as np

def brute_force(n, ri):
    def get_permutations_itertools(n):
        numbers = list(range(n))
        perms = [list(p) for p in permutations(numbers)]
        return perms

    # n = int(input())
    # ri = list(map(float, input().split(", ")))
    best_result, best_order = 0, []
    for order in get_permutations_itertools(n):
        result = 0
        for t in range(n):
            result += 100 * ri[order[t]] ** (t + 1)
        if result > best_result:
            best_result = result
            best_order = order

    print(f"--[bf]--best_order: {[ri[i] for i in best_order]}")
    return best_result

def losses(t_start, n, ri):
    # t_start = int(input("Начальное время: "))
    # n = int(input("Кол-во оборудования: "))
    # ri = list(map(float, input("Коэффициенты: ").split(", ")))  # Коэффициенты скорости падения цены

    best_order = []

    for t in range(t_start, t_start + n - 1):
        # Список потерь - это сумма, которую мы потеряем, если не продадим i-й элемент сейчас
        losses = list(map(lambda x: (100 * x ** t) - (100 * x ** (t + 1)), ri))
        best_order.append(ri.pop(losses.index(max(losses))))
    best_order.append(ri[0])

    print(f"--[ls]--best_order: {best_order}")
    return sum(100 * best_order[i] ** (t_start + i) for i in range(n))

def testing(n_tests, upper_lim):
    T_START = 1
    np.random.seed(42)


    for i in range(n_tests):
        n = int(np.random.random() * upper_lim) + 2
        ri = list(map(float, np.round(np.random.random((1, n))[0], 2)))
        print(f"ТЕСТ {i + 1}")
        print(f"Входные данные: {n, ri}")
        bf_result = np.round(brute_force(n, ri), 2)
        ls_result = np.round(losses(T_START, n, ri), 2)

        print(f"brute_force: {bf_result}, losses: {ls_result}")
        if bf_result != ls_result:
            return False

    return True


if __name__ == "__main__":
    n_tests = int(input())
    upper_lim = int(input())
    print("Успех" if testing(n_tests, upper_lim) else "Неверный ответ")
    # 10 10 - Ошибка