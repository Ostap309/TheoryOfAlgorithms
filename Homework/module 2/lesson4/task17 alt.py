n = int(input())
ri = list(map(float, input().split(", ")))
remaining_product = list(range(n))
best_order = []
for t in range(1, n):
    losses = list(map(lambda x: 100 * x ** t - 100 * x ** (t + 1), ri))
    best_ind = losses.index(max(losses))
    best_order.append(remaining_product.pop(best_ind))
    print(losses)
