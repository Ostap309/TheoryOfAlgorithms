def dynamic_programming_solver(n, x, r):
    points = sorted(zip(x, r))
    x_sorted = [p[0] for p in points]
    r_sorted = [p[1] for p in points]

    dp = [0] * (n + 1)
    dp[1] = r_sorted[0]

    for i in range(2, n + 1):
        current_x = x_sorted[i - 1]
        current_r = r_sorted[i - 1]

        j = find_last_valid_point(x_sorted, current_x - 5, i - 1)

        dp[i] = max(dp[i - 1], current_r + dp[j + 1])

    return dp[n]


def find_last_valid_point(x, target, max_index):
    left, right = 0, max_index
    result = -1
    while left <= right:
        mid = (left + right) // 2
        if x[mid] < target:
            result = mid
            left = mid + 1
        else:
            right = mid - 1
    return result


if __name__ == '__main__':
    n = int(input())
    x = list(map(int, input().split()))
    r = list(map(int, input().split()))
    print(dynamic_programming_solver(n, x, r))
