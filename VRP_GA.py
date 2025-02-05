import random
import numpy as np


# Випадкова відстань між містами (симуляція карти)
def generate_distance_matrix(n):
    matrix = np.random.randint(10, 100, size=(n, n))
    np.fill_diagonal(matrix, 0)  # Немає відстані між містом і собою
    return matrix


# Функція оцінки маршруту (загальна довжина маршруту)
def fitness(route, distance_matrix):
    total_distance = sum(distance_matrix[route[i]][route[i + 1]] for i in range(len(route) - 1))
    total_distance += distance_matrix[route[-1]][route[0]]  # Повернення у стартове місто
    return total_distance


# Жадібна ініціалізація популяції
def nearest_neighbor(n, distance_matrix):
    start = random.randint(0, n - 1)
    unvisited = set(range(n))
    unvisited.remove(start)
    route = [start]

    while unvisited:
        nearest = min(unvisited, key=lambda city: distance_matrix[route[-1]][city])
        route.append(nearest)
        unvisited.remove(nearest)

    return route


# Ordered Crossover (OX)
def crossover(parent1, parent2):
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))

    child = [-1] * size
    child[start:end] = parent1[start:end]

    p2_idx = end
    c_idx = end

    while -1 in child:
        if parent2[p2_idx % size] not in child:
            child[c_idx % size] = parent2[p2_idx % size]
            c_idx += 1
        p2_idx += 1

    return child


# Swap Mutation (обмін двох випадкових міст)
def mutate(route):
    i, j = random.sample(range(len(route)), 2)
    route[i], route[j] = route[j], route[i]
    return route


# 2-opt локальна оптимізація
def two_opt(route, distance_matrix):
    best = route
    best_cost = fitness(route, distance_matrix)
    improved = True

    while improved:
        improved = False
        for i in range(1, len(route) - 2):
            for j in range(i + 1, len(route)):
                if j - i == 1: continue  # Не міняємо сусідні міста

                new_route = route[:i] + route[i:j][::-1] + route[j:]
                new_cost = fitness(new_route, distance_matrix)

                if new_cost < best_cost:
                    best = new_route
                    best_cost = new_cost
                    improved = True

    return best


# Основний генетичний алгоритм
def genetic_algorithm(n, distance_matrix, pop_size=100, generations=200, mutation_rate=0.2):
    # Генеруємо початкову популяцію
    population = [nearest_neighbor(n, distance_matrix) for _ in range(pop_size)]

    for gen in range(generations):
        population = sorted(population, key=lambda route: fitness(route, distance_matrix))
        new_population = population[:10]  # Найкращі рішення зберігаємо

        while len(new_population) < pop_size:
            parent1, parent2 = random.sample(population[:50], 2)  # Відбір кращих батьків
            child = crossover(parent1, parent2)

            if random.random() < mutation_rate:
                child = mutate(child)

            child = two_opt(child, distance_matrix)  # Оптимізація 2-opt
            new_population.append(child)

        population = new_population
        best_route = population[0]
        best_cost = fitness(best_route, distance_matrix)
        print(f"Покоління {gen + 1}: Найкращий маршрут {best_cost}")

    return population[0], fitness(population[0], distance_matrix)


# Запуск
n_cities = 10
distance_matrix = generate_distance_matrix(n_cities)

best_route, best_cost = genetic_algorithm(n_cities, distance_matrix)
print("\nНайкращий маршрут:", best_route)
print("Мінімальна вартість:", best_cost)
