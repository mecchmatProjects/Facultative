import itertools
import heapq
import numpy as np


class VRP_BranchAndBound:
    def __init__(self, distance_matrix, vehicle_capacity, demands, depot=0):
        self.distance_matrix = distance_matrix
        self.vehicle_capacity = vehicle_capacity
        self.demands = demands
        self.depot = depot
        self.num_nodes = len(distance_matrix)
        self.best_cost = float('inf')
        self.best_route = None

    def lower_bound(self, route):
        cost = sum(self.distance_matrix[route[i]][route[i + 1]] for i in range(len(route) - 1))
        remaining_nodes = set(range(self.num_nodes)) - set(route)

        if remaining_nodes:
            edges = [self.distance_matrix[i][j] for i in remaining_nodes for j in remaining_nodes if i != j]
            if edges:
                min_edge_cost = min(edges)
            else:
                min_edge_cost = float('inf')  # Якщо немає доступних переходів


            min_edge_cost = min(
                (self.distance_matrix[i][j] for i in remaining_nodes for j in remaining_nodes if i != j),
                default=float('inf')  # Додає значення за замовчуванням
            )
            cost += min_edge_cost


        return cost

    def branch_and_bound(self):
        pq = []  # Priority queue
        initial_route = [self.depot]
        heapq.heappush(pq, (0, initial_route, 0, 0))  # (bound, route, load, cost)

        while pq:
            bound, route, load, cost = heapq.heappop(pq)

            if cost >= self.best_cost:
                continue

            if len(route) == self.num_nodes:
                total_cost = cost + self.distance_matrix[route[-1]][self.depot]
                if total_cost < self.best_cost:
                    self.best_cost = total_cost
                    self.best_route = route + [self.depot]
                continue

            for next_node in range(self.num_nodes):
                if next_node in route:
                    continue

                new_load = load + self.demands[next_node]
                if new_load > self.vehicle_capacity:
                    continue

                new_route = route + [next_node]
                new_cost = cost + self.distance_matrix[route[-1]][next_node]
                new_bound = new_cost + self.lower_bound(new_route)

                if new_bound < self.best_cost:
                    heapq.heappush(pq, (new_bound, new_route, new_load, new_cost))

        return self.best_route, self.best_cost


# Приклад використання
distance_matrix = np.array([
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
])

demands = [0, 10, 10, 10]  # Запити клієнтів
vehicle_capacity = 20

def check_cost_matrix(cost_matrix):
    n = len(cost_matrix)
    for i in range(n):
        for j in range(n):
            if i != j and (cost_matrix[i][j] <= 0 or cost_matrix[i][j] == float('inf')):
                print(f"⚠️ Некоректна вага між {i} і {j}: {cost_matrix[i][j]}")

check_cost_matrix(distance_matrix)

vrp_solver = VRP_BranchAndBound(distance_matrix, vehicle_capacity, demands)
best_route, best_cost = vrp_solver.branch_and_bound()

print("Найкращий маршрут:", best_route)
print("Мінімальна вартість:", best_cost)
