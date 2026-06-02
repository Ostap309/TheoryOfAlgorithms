def dynamic_programming_graph_solver(weights):
    n = len(weights)
    if n == 0:
        return [], 0
    if n == 1:
        return [1], weights[0]

    dp = [0] * (n + 1)
    dp[1] = weights[0]

    for i in range(2, n + 1):
        dp[i] = max(dp[i - 1], dp[i - 2] + weights[i - 1])

    indices = []
    i = n
    while i > 0:
        if dp[i] != dp[i - 1]:
            indices.append(i)
            i -= 2
        else:
            i -= 1

    indices.reverse()
    return indices, dp[n]


if __name__ == "__main__":
    weights = list(map(int, input().split()))
    vert_ind, max_weight = dynamic_programming_graph_solver(weights)
    print(vert_ind)
    print(max_weight)
