import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import time

SEED = 42  # Случайное начальное число
PROBABILITY = 0.3  # Вероятность появления ребра
N_RANGE = range(5, 3000, 10)  # Количество вершин
RETESTS = 5  # Количество испытаний для каждого числа вершин

times_mean = []  # среднее время выполнения
times_std = []  # среднее квадратичное отклонение по времени выполнения

times = np.array([None] * RETESTS)  # Массив фактического времени выполнения длины RETESTS
pointer = 0  # Указатель на индекс массива times


# Декоратор, измеряющий время исполнения алгоритма
def measure_execution_time(func):
    def wrapper(*args, **kwargs):
        global times, pointer

        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        times[pointer] = execution_time
        pointer = (pointer + 1) % RETESTS

        return result

    return wrapper


@measure_execution_time
def algorithm(graph: nx.Graph):
    return len(nx.maximal_independent_set(graph))

    # pos = nx.spring_layout(graph)
    # nx.draw(graph, pos, with_labels=True, node_color='lightblue', node_size=500)
    # plt.title("Граф Эрдеша‑Реньи (seed=42)")
    # plt.show()


# Создание графов, запуск алгоритма, построение графика производительности
def main():
    global times_mean, times_std, times

    for n in N_RANGE:
        new_graph = nx.erdos_renyi_graph(n, p=PROBABILITY, seed=SEED)

        for _ in range(RETESTS):
            algorithm(new_graph)
            # quit()

        times_mean.append(times.mean())
        times_std.append(times.std())

    print(times_mean)
    print(times_std)

    plt.scatter(N_RANGE, times_mean)
    plt.show()


if __name__ == '__main__':
    main()
