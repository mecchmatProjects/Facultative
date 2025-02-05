import numpy as np
import heapq


def tsp_mst_approximation(cost_matrix):
    n = len(cost_matrix)
    # Перевірка, що вартість не є нульовою
    if n == 0:
        return [], 0

    # Побудова MST за допомогою алгоритму Прима
    # Використовуємо масив visited для позначення відвіданих вузлів
    visited = [False] * n
    min_heap = [(0, 0)]  # (вага, вузол), починаємо з вузла 0
    mst_cost = 0
    mst_edges = []

    while min_heap:
        cost, u = heapq.heappop(min_heap)
        if visited[u]:
            continue
        visited[u] = True
        mst_cost += cost

        for v in range(n):
            if not visited[v] and cost_matrix[u][v] != 0:
                heapq.heappush(min_heap, (cost_matrix[u][v], v))
                mst_edges.append((u, v))

    # Повертаємо приблизний шлях, використовуючи обхід DFS по MST
    path = []

    def dfs(node):
        path.append(node)
        visited[node] = True
        for u, v in mst_edges:
            if u == node and not visited[v]:
                dfs(v)
            elif v == node and not visited[u]:
                dfs(u)

    # Запускаємо DFS з початкового вузла (наприклад, вузол 0)
    visited = [False] * n
    dfs(0)
    path.append(path[0])  # Повертаємося до початкового вузла, щоб завершити цикл

    # Розрахунок вартості шляху комівояжера
    tsp_cost = sum(cost_matrix[path[i]][path[i + 1]] for i in range(n))

    return path, tsp_cost


# Приклад використання
cost_matrix = [
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
]

approx_path, approx_cost = tsp_mst_approximation(cost_matrix)
print("Приблизний шлях:", approx_path)
print("Приблизна вартість:", approx_cost)
