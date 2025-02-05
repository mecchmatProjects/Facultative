from scipy.optimize import linprog

# Коефіцієнти цільової функції (вартість компонентів)
c = [3, 5]

# Коєфіцієнти обмежень
A = [
    [-2, -8],  # -2x - 8y >= -40
    [-4, -2]   # -4x - 2y >= -30
]

# Права частина обмежень
b = [-40, -30]

# Ax <= b

# Обмеження на те, що кількість компонентів не може бути від'ємною
x_bounds = (0, None)
y_bounds = (0, None)

# Виконання оптимізації
result = linprog(c, A_ub=A, b_ub=b, bounds=[x_bounds, y_bounds], method='highs')

if result.success:
    print("Оптимальне значення витрат:", result.fun)
    print("Оптимальна кількість зерна (x):", result.x[0])
    print("Оптимальна кількість м'ясних відходів (y):", result.x[1])
else:
    print("Розв'язок не знайдено.")
