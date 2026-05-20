from collections import defaultdict

class DSU:
    def __init__(self, n):
        self.parent = [-1] * n  # отрицательное число - признак корня, положительное - ссылка на родителя

    def find(self, x):
        # Отрицательный индекс. Поиск достиг корня
        if self.parent[x] < 0:
            return x

        # Неотрицательный индекс (он же индекс родителя). Поиск повторяется, но уже от родителя
        root = self.find(self.parent[x])
        self.parent[x] = root  # сжатие пути
        return root

    def union(self, x, y):
        rootX = self.find(x)
        rootY = self.find(y)

        if rootX == rootY:
            return  # уже в одном множестве

        # подвешиваем дерево с меньшей глубиной к дереву с большей глубиной
        if self.parent[rootX] < self.parent[rootY]:
            self.parent[rootY] += self.parent[rootX]
            self.parent[rootX] = rootY
        else:
            self.parent[rootX] += self.parent[rootY]
            self.parent[rootY] = rootX

        return



def main():
    n, k = map(int, input().split())
    dsu = DSU(n)

    # Условимся, что дороги, контролируемые Бани Яс (Б), вводятся первыми.
    input() # Бани Яс
    line = input()
    while line[0] != 'А':
        u, v = map(int, line.split())
        dsu.union(u, v)

        line = input()


    A_relations_dict = defaultdict(int)
    countA_min = len([i for i in dsu.parent if i < 0]) - 1

    if k < countA_min:
        print("k не достижимо. Для связности требуется включить больше дорог, подконтрольных Аназа!")
        return

    line = input()
    while line[0] != '-':
        u, v = map(int, line.split())
        root_u, root_v = dsu.find(u), dsu.find(v)
        root_min, root_max = min(root_u, root_v), max(root_u, root_v)
        A_relations_dict[(root_min, root_max)] += 1

        line = input()

    # Реализуем поиск максимального пути по алгоритму Крускала
    A_relations_dict = dict(sorted(A_relations_dict.items(), key=lambda item: item[1], reverse=True))

    countA_max = 0
    for vertices, weight in A_relations_dict.items():
        if dsu.find(vertices[0]) != dsu.find(vertices[1]):
            countA_max += weight
            dsu.union(vertices[0], vertices[1])

    print(f"Диапазон k: [{countA_min}, {countA_max}]")

    if k > countA_max:
        print("k не достижимо. На графе недостаточно дорог, подконтрольных Аназа!")
        return

    print("Можно взять k дорог!")

if __name__ == '__main__':
    main()