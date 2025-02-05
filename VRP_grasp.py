import random
import math

# Параметри задачі
NUM_CUSTOMERS = 20  # Кількість клієнтів
NUM_VEHICLES = 3    # Кількість транспортних засобів
VEHICLE_CAPACITY = 50  # Вантажопідйомність кожного транспортного засобу
MAX_ITERATIONS = 100  # Максимальна кількість ітерацій GRASP
ALPHA = 0.5  # Параметр для випадкового вибору (0 < ALPHA < 1)

# Координати депо та клієнтів (випадкові значення)
depot = (0, 0)
customers = [(random.uniform(-50, 50), random.uniform(-50, 50)) for _ in range(NUM_CUSTOMERS)]
demands = [random.randint(1, 10) for _ in range(NUM_CUSTOMERS)]  # Випадкові потреби клієнтів

# Функція для обчислення відстані між двома точками
def distance(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

# Функція для побудови початкового розв'язку (жадібний алгоритм з випадковістю)
def construct_greedy_randomized_solution():
    routes = [[] for _ in range(NUM_VEHICLES)]
    remaining_customers = set(range(NUM_CUSTOMERS))
    remaining_capacity = [VEHICLE_CAPACITY] * NUM_VEHICLES

    while remaining_customers:
        for vehicle in range(NUM_VEHICLES):
            if not remaining_customers:
                break

            # Список доступних клієнтів, які можна додати до маршруту
            feasible_customers = [
                c for c in remaining_customers
                if demands[c] <= remaining_capacity[vehicle]
            ]

            if not feasible_customers:
                continue

            # Обчислення вартості додавання кожного клієнта
            costs = []
            for c in feasible_customers:
                last_node = depot if not routes[vehicle] else customers[routes[vehicle][-1]]
                cost = distance(last_node, customers[c])
                costs.append((c, cost))

            # Вибір клієнта з обмеженим списком кращих варіантів
            min_cost = min(c[1] for c in costs)
            max_cost = max(c[1] for c in costs)
            threshold = min_cost + ALPHA * (max_cost - min_cost)
            candidate_list = [c for c in costs if c[1] <= threshold]

            # Випадковий вибір клієнта з кандидатів
            chosen_customer, _ = random.choice(candidate_list)

            # Додавання клієнта до маршруту
            routes[vehicle].append(chosen_customer)
            remaining_capacity[vehicle] -= demands[chosen_customer]
            remaining_customers.remove(chosen_customer)

    return routes

# Функція для обчислення загальної вартості маршрутів
def calculate_total_cost(routes):
    total_cost = 0
    for route in routes:
        if not route:
            continue
        # Відстань від депо до першого клієнта
        total_cost += distance(depot, customers[route[0]])
        # Відстань між клієнтами
        for i in range(1, len(route)):
            total_cost += distance(customers[route[i - 1]], customers[route[i]])
        # Відстань від останнього клієнта до депо
        total_cost += distance(customers[route[-1]], depot)
    return total_cost

# Функція для локального пошуку (покращення розв'язку)
def local_search(routes):
    improved = True
    while improved:
        improved = False
        for i in range(len(routes)):
            for j in range(len(routes[i]) - 1):
                # Спробуємо поміняти місцями двох клієнтів
                new_route = routes[i].copy()
                new_route[j], new_route[j + 1] = new_route[j + 1], new_route[j]
                new_cost = calculate_total_cost([new_route] + routes[:i] + routes[i + 1:])
                if new_cost < calculate_total_cost(routes):
                    routes[i] = new_route
                    improved = True
    return routes

# Основна функція GRASP
def grasp_vrp():
    best_solution = None
    best_cost = float('inf')

    for _ in range(MAX_ITERATIONS):
        # Побудова початкового розв'язку
        solution = construct_greedy_randomized_solution()
        # Покращення розв'язку локальним пошуком
        solution = local_search(solution)
        # Обчислення вартості
        cost = calculate_total_cost(solution)
        # Оновлення найкращого розв'язку
        if cost < best_cost:
            best_solution = solution
            best_cost = cost

    return best_solution, best_cost

# Виконання GRASP
best_routes, best_cost = grasp_vrp()
print("Найкращі маршрути:", best_routes)
print("Загальна вартість:", best_cost)