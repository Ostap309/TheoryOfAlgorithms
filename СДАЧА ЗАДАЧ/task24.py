from collections import defaultdict, deque

class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = defaultdict(list)

    def add_edge(self, u, v, cost):
        self.graph[u].append((v, cost))
        self.graph[v].append((u, cost))

def find_path_in_tree(tree, start, end):
    if start == end:
        return []

    visited = set()
    queue = deque([(start, [])])

    while queue:
        current, path = queue.popleft()

        if current in visited:
            continue

        visited.add(current)

        for neighbor, cost in tree.graph[current]:
            new_path = path + [(current, neighbor, cost)]

            if neighbor == end:
                return new_path

            if neighbor not in visited:
                queue.append((neighbor, new_path))

    return []

def is_mst_still_optimal(tree, v, w, new_cost):
    path = find_path_in_tree(tree, v, w)

    if not path:
        raise ValueError("В дереве должен существовать путь между v и w")

    max_cost_on_path = max(edge[2] for edge in path)

    if new_cost >= max_cost_on_path:
        return True
    else:
        return False

if __name__ == "__main__":
    T = Graph(4)
    T.add_edge(0, 1, 2)
    T.add_edge(1, 2, 3)
    T.add_edge(2, 3, 4)

    result1 = is_mst_still_optimal(T, 0, 3, 5)
    print(f"Случай 1 (c=5): {result1}")

    result2 = is_mst_still_optimal(T, 0, 3, 3)
    print(f"Случай 2 (c=3): {result2}")
