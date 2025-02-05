import numpy as np
from queue import PriorityQueue


class Node:
    def __init__(self, level, path, bound):
        self.level = level  # Поточний рівень дерева
        self.path = path  # Поточний маршрут
        self.bound = bound  # Нижня межа (мінімальна можлива вартість)

    def __lt__(self, other):
        return self.bound < other.bound  # Пріоритет у вузла з меншою межею


def calculate_lower_bound(cost_matrix, path, n):
    """ Обчислення нижньої межі (мінімальної можливої вартості) """
    bound = 0
    included = set(path)

    for i in range(n):
        if i in included and len(path) > 1:
            continue  # Пропускаємо вже відвідані вершини

        min1, min2 = float('inf'), float('inf')
        for j in range(n):
            if i == j:
                continue
            cost = cost_matrix[i][j]
            if cost < min1:
                min2 = min1
                min1 = cost
            elif cost < min2:
                min2 = cost

        # Додаємо два мінімальних ребра для кожної вершини
        if min1 < float('inf') and min2 < float('inf'):
            bound += (min1 + min2) / 2

    return bound


def branch_and_bound_vrp(cost_matrix):
    """ Реалізація VRP методом відгалужень і меж """
    n = len(cost_matrix)
    pq = PriorityQueue()  # Черга з пріоритетами
    min_cost = float('inf')  # Найменша знайдена вартість
    best_path = None  # Найкращий маршрут

    # Початковий вузол
    start_node = Node(level=0, path=[0], bound=calculate_lower_bound(cost_matrix, [0], n))
    pq.put(start_node)

    while not pq.empty():
        node = pq.get()  # Беремо вузол з найменшою нижньою межею

        if node.bound >= min_cost:
            continue  # Відсікаємо гілки, які гарантовано не покращать результат

        # Якщо досягли останнього рівня (відвідали всі міста)
        if node.level == n - 1:
            last_city = node.path[-1]
            if cost_matrix[last_city][0] < float('inf'):  # Повернення в депо
                final_cost = sum(cost_matrix[node.path[i]][node.path[i + 1]] for i in range(n - 1)) + \
                             cost_matrix[last_city][0]
                if final_cost < min_cost:
                    min_cost = final_cost
                    best_path = node.path + [0]  # Додаємо повернення

        else:
            # Генеруємо дочірні вузли для кожної можливої наступної вершини
            for next_city in range(n):
                if next_city not in node.path and cost_matrix[node.path[-1]][next_city] < float('inf'):
                    new_path = node.path + [next_city]
                    new_bound = calculate_lower_bound(cost_matrix, new_path, n)

                    if new_bound < min_cost:  # Якщо потенційний маршрут кращий, додаємо його в чергу
                        pq.put(Node(node.level + 1, new_path, new_bound))

    return best_path, min_cost


# Тестова матриця вартостей (відстаней)
cost_matrix = [
    [float('inf'), 10, 15, 20],
    [10, float('inf'), 35, 25],
    [15, 35, float('inf'), 30],
    [20, 25, 30, float('inf')]
]

best_path, min_cost = branch_and_bound_vrp(cost_matrix)

print("Найкращий маршрут:", best_path)
print("Мінімальна вартість:", min_cost)
