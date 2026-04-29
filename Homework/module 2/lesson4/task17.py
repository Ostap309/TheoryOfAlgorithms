from itertools import permutations


def get_permutations_itertools(n):
    numbers = list(range(n))
    perms = [list(p) for p in permutations(numbers)]
    return perms


n = int(input())
ri = list(map(float, input().split(", ")))
best_result, best_order = 0, []
for order in get_permutations_itertools(n):
    result = 0
    for t in range(n):
        result += 100 * ri[order[t]] ** (t + 1)
        print(" +", 100 * ri[order[t]] ** (t + 1))
    if result > best_result:
        best_result = result
        best_order = order

    print(result, "|", " -> ".join(map(lambda x: str(ri[x]), order)))
    print()

print("=========\nBEST:")
print(best_result, "|", " -> ".join(map(lambda x: str(ri[x]), best_order)))
