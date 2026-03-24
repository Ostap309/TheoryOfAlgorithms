import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import time
import threading
import sys

SEED = 42  # Случайное начальное число
PROBABILITY = 0.1  # Вероятность появления ребра
N_RANGE = range(5, 1001, 3)  # Количество вершин
DRAW_AND_QUIT = -1  # Преждевременная остановка с визуализацией графа (-1 - откл.)
RETESTS = 10  # Количество испытаний для каждого числа вершин
MAX_RUNTIME = 100
STOP_NOW = False

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
        """Объект хранит список связности и количество вершин графа (см. Идея 2 Список связности)"""
        self.conlist = []
        self.length = graph.number_of_nodes()
        # Для каждой вершины будем хранить маску связности в списке связности по индексу с номером этой вершины
        for node in range(self.length):
            self.conlist.append(self.to_binary(graph.neighbors(node)))

    @staticmethod
    def to_binary(neighbors) -> int:
        """Метод создает на основе итератора битовую маску, где каждый бит хранит связь текущей вершины с i-м соседом"""
        binary = 0

        # Создаем маску связности
        for i in neighbors:
            binary |= 1 << i
        return binary

    def __str__(self) -> str:
        """Метод создает текстовое представление списка связности"""
        res_str = ""
        for node, mask in enumerate(self.conlist):
            res_str += f"{node}: {bin(mask)}\n"

        return res_str

    def check_independence(self, subset: int) -> bool:
        """Метод проверяет независимость элементов подмножества с помощью маски соседей (см. Идея 1 Битовая маска)"""
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
    global STOP_NOW

    cl = ConnectivityList(graph)
    misl = 1  # max independent set length (искомое значение)

    independent_subsets = [0, 1]
    step = 1
    while step < cl.length:
        l = len(independent_subsets)
        for i in range(l):
            if STOP_NOW:
                output()
            # Добавляем к подмножеству новую вершину
            new_subset = independent_subsets[i] | (1 << step)

            # Проверка на независимость
            if cl.check_independence(new_subset):
                nodes_count = new_subset.bit_count()
                if nodes_count > misl:
                    misl = nodes_count

                # Добавляем только "перспективные" подмножества
                if nodes_count + cl.length - step - 1 > misl:
                    independent_subsets.append(new_subset)
        step += 1

    return misl


def stop():
    global STOP_NOW
    STOP_NOW = True


# Создание графов, запуск алгоритма, построение графика производительности
def main():
    global times_mean, times_std, times

    timer = threading.Timer(MAX_RUNTIME * 60, stop)
    timer.start()

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
                timer.cancel()
                sys.exit(0)

        times_mean.append(times.mean())
        times_std.append(times.std())

    timer.cancel()
    output()


def output():
    global times_mean, times_std

    print(times_mean)
    print(times_std)

    plt.plot(list(N_RANGE[:len(times_mean)]), times_mean)
    plt.show()

    sys.exit(0)


if __name__ == '__main__':
    main()
