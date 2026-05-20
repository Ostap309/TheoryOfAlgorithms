t_start = int(input("Начальное время: "))
n = int(input("Кол-во оборудования: "))
ri = list(map(float, input("Коэффициенты: ").split(", ")))  # Коэффициенты скорости падения цены

best_order = []

for t in range(t_start, t_start + n - 1):
    # Список потерь - это сумма, которую мы потеряем, если не продадим i-й элемент сейчас
    losses = list(map(lambda x: (100 * x ** t) - (100 * x ** (t + 1)), ri))
    best_order.append(ri.pop(losses.index(max(losses))))
best_order.append(ri[0])

print(best_order, "Сумма:", sum(100 * best_order[i] ** (t_start + i) for i in range(n)))
