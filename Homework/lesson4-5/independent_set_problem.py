import networkx as nx
import matplotlib.pyplot as plt
import time

inputs_num_list = []
times_list = []


# Декоратор, измеряющий время исполнения алгоритма
def measure_execution_time(func):
    def wrapper(*args, **kwargs):
        global times_list

        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        times_list.append(execution_time)

        return result

    return wrapper


@measure_execution_time
def algorithm(graph: nx.Graph):
    pass


# Создание графов, запуск алгоритма, построение графика производительности
def main():
    global inputs_num_list

    SEED = 42
    PROBABILITY = 0.3

    for n in range(5, 1000, 10):
        new_graph = nx.erdos_renyi_graph(n, p=PROBABILITY, seed=SEED)

        inputs_num_list.append(n)
        algorithm(new_graph)

    print(inputs_num_list)
    print(times_list)

    plt.scatter(inputs_num_list, times_list)
    plt.show()


if __name__ == '__main__':
    main()
