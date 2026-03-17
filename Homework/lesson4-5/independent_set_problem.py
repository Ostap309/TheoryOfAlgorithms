import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import time

SEED = 42  # Случайное начальное число
PROBABILITY = 0.1  # Вероятность появления ребра
N_RANGE = range(5, 21)  # Количество вершин
DRAW_AND_QUIT = -1 # Преждевременная остановка с визуализацией графа (-1 - откл.)
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


class ConnectivityList:
    def __init__(self, graph: nx.Graph):
        self.conlist = []
        self.length = graph.number_of_nodes()
        # Для каждой вершины будем хранить маску связности в списке связности по индексу с номером этой вершины
        for node in range(self.length):
            self.conlist.append(self.to_binary(graph.neighbors(node)))

    @staticmethod
    def to_binary(neighbors) -> int:
        binary = 0

        # Создаем маску связности
        for i in neighbors:
            binary |= 1 << i
        return binary

    def __str__(self) -> str:
        res_str = ""
        for node, mask in enumerate(self.conlist):
            res_str += f"{node}: {bin(mask)}\n"

        return res_str

    def check_independence(self, subset: int) -> bool:
        neighbors_mask = 0
        temp = subset
        index = 0
        while temp:
            if temp & 1:
                neighbors_mask |= self.conlist[index]
            temp >>= 1
            index += 1

        if not neighbors_mask & subset:
            return True

        return False


@measure_execution_time
def algorithm(graph: nx.Graph) -> int:
    cl = ConnectivityList(graph)
    misl = 0  # max independent set length (искомое значение)

    cur_subset = 1
    while cur_subset <= (1 << cl.length) - 1:
        if cl.check_independence(cur_subset):
            nodes_count = cur_subset.bit_count()
            if nodes_count > misl:
                misl = nodes_count
        cur_subset += 1

    return misl


# Создание графов, запуск алгоритма, построение графика производительности
def main():
    global times_mean, times_std, times

    for n in N_RANGE:
        graph = nx.erdos_renyi_graph(n, p=PROBABILITY, seed=SEED)

        # Объявляем новый порядок вершин по возрастанию степеней
        node_order = [node for node, _ in sorted(dict(graph.degree()).items(), key=lambda x: x[1])]
        # Сопоставляем каждой вершине её новое название
        mapping = {old: new for new, old in enumerate(node_order)}
        # переименовываем вершены, сохраняем полученную копию в новую переменную
        sorted_graph = nx.relabel_nodes(graph, mapping)

        for _ in range(RETESTS):
            result = algorithm(sorted_graph)

            if DRAW_AND_QUIT != -1 and n >= DRAW_AND_QUIT:
                print(result)
                pos = nx.spring_layout(sorted_graph)
                nx.draw(sorted_graph, pos, with_labels=True, node_color='lightblue', node_size=500)
                plt.show()
                quit()

        times_mean.append(times.mean())
        times_std.append(times.std())

    # print(times_mean)
    # print(times_std)

    plt.plot(N_RANGE, times_mean)
    plt.show()


if __name__ == '__main__':
    main()
