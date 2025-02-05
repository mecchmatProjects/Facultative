import numpy as np
import heapq

class Node:
    def __init__(self, level, path, bound):
        self.level = level    # Рівень у дереві
        self.path = path      # Маршрут на цьому вузлі
        self.bound = bound    # Межа для даного вузла

    # Для порівняння вузлів у черзі з пріоритетом
    def __lt__(self, other):
        return self.bound < other.bound

def tsp_branch_and_bound(cost_matrix):
    n = len(cost_matrix)
    # Початкові налаштування
    priority_queue = []
    root = Node(0, [0], calculate_bound(cost_matrix, [0]))
    heapq.heappush(priority_queue, root)
    best_cost = float('inf')
    best_path = []

    while priority_queue:
        node = heapq.heappop(priority_queue)

        # Якщо повний маршрут знайдено
        if node.level == n - 1:
            current_path_cost = calculate_cost(cost_matrix, node.path + [0])
            if current_path_cost < best_cost:
                best_cost = current_path_cost
                best_path = node.path + [0]

        # Розгалуження вузла
        if node.bound < best_cost:
            for i in range(n):
                if i not in node.path:
                    new_path = node.path + [i]
                    bound = calculate_bound(cost_matrix, new_path)
                    if bound < best_cost:
                        heapq.heappush(priority_queue, Node(node.level + 1, new_path, bound))

    return best_path, best_cost

def calculate_bound(cost_matrix, path):
    n = len(cost_matrix)
    bound = 0

    # Додаємо вартість пройденого маршруту
    for i in range(len(path) - 1):
        bound += cost_matrix[path[i]][path[i + 1]]

    # Оцінка мінімальної вартості для решти міст
    for i in range(n):
        if i not in path:
            min_cost = min(cost_matrix[i][j] for j in range(n) if j != i)
            bound += min_cost

    return bound

def calculate_cost(cost_matrix, path):
    cost = 0
    for i in range(len(path) - 1):
        cost += cost_matrix[path[i]][path[i + 1]]
    return cost

# Приклад використання
cost_matrix = [
    [0, 20, 42, 35],
    [20, 0, 30, 34],
    [42, 30, 0, 12],
    [35, 34, 12, 0]
]

best_path, best_cost = tsp_branch_and_bound(cost_matrix)
print("Найкращий маршрут:", best_path)
print("Мінімальна вартість:", best_cost)
