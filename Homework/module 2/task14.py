from collections import defaultdict, deque


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
    n, m = map(int, input().split())
    dsu = DSU(n)

    different_pairs = []
    for _ in range(m):
        u, v, rel = input().split()
        u = int(u)
        v = int(v)

        if rel == 'о':
            dsu.union(u, v)
        else:
            different_pairs.append((u, v))

    # Если все вершины образуют связный граф, то их нельзя разбить на 2 вида по компонентам
    if dsu.parent[dsu.find(0)] == -1 * n:
        return False

    # строим двудольный граф отношений «разные» между компонентами
    graph = defaultdict(set)

    for u, v in different_pairs:
        root_u, root_v = dsu.find(u), dsu.find(v)
        # Если вершины в одной компоненте - противоречие
        if root_u == root_v:
            return False
        graph[root_u].add(root_v)
        graph[root_v].add(root_u)

    # Проверка двудольности графа компонентов
    color = {}  # 0 или 1

    def bfs(start):
        queue = deque([start])
        color[start] = 0

        while queue:
            node = queue.popleft()
            for neighbor in graph[node]:
                if neighbor not in color:
                    color[neighbor] = color[node] ^ 1
                    queue.append(neighbor)
                elif color[neighbor] == color[node]:
                    return False
        return True

    # Проверяем все компоненты
    for component in graph:
        if component not in color:
            if not bfs(component):
                return False

    return True


print("Разбиение возможно" if main() else "Противоречие")
