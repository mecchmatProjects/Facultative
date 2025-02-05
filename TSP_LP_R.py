from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpBinary, PULP_CBC_CMD


def tsp_lp(cost_matrix):
    n = len(cost_matrix)

    # Створюємо модель лінійного програмування
    model = LpProblem("TSP", LpMinimize)

    # Змінні: x[i][j] = 1, якщо ми переходимо з міста i в місто j, інакше 0
    x = [[LpVariable(f"x_{i}_{j}", cat=LpBinary) for j in range(n)] for i in range(n)]

    # Цільова функція: мінімізувати загальну відстань
    model += lpSum(cost_matrix[i][j] * x[i][j] for i in range(n) for j in range(n) if i != j)

    # Кожне місто має мати рівно один вхідний і один вихідний шлях
    for i in range(n):
        model += lpSum(x[i][j] for j in range(n) if i != j) == 1  # рівно один вихід
        model += lpSum(x[j][i] for j in range(n) if i != j) == 1  # рівно один вхід

    # Обмеження підзадачі (використовується метод підтурів для уникнення нецільових циклів)
    u = [LpVariable(f"u_{i}", lowBound=0, cat="Continuous") for i in range(n)]
    for i in range(1, n):
        for j in range(1, n):
            if i != j:
                model += u[i] - u[j] + n * x[i][j] <= n - 1

    # Розв'язуємо модель
    model.solve(PULP_CBC_CMD(msg=False))

    # Збираємо результат
    tour = []
    for i in range(n):
        for j in range(n):
            if x[i][j].varValue == 1:
                tour.append((i, j))

    # Формуємо шлях на основі турів
    result_path = [0]
    while len(result_path) < n:
        for i, j in tour:
            if i == result_path[-1]:
                result_path.append(j)
                break

    return result_path, model.objective.value()


# Приклад використання
cost_matrix = [
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
]

best_path, best_cost = tsp_lp(cost_matrix)
print("Оптимальний шлях:", best_path)
print("Мінімальна вартість:", best_cost)