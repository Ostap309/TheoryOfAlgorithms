def find_peak_element(arr):
    n = len(arr)

    if n == 1:
        return 0
    if arr[0] > arr[1]:
        return 0
    if arr[n - 1] > arr[n - 2]:
        return n - 1

    left, right = 0, n - 1

    while left <= right:
        mid = (left + right) // 2

        is_peak = True
        if mid > 0 and arr[mid] <= arr[mid - 1]:
            is_peak = False
        if mid < n - 1 and arr[mid] <= arr[mid + 1]:
            is_peak = False

        if is_peak:
            return mid

        elif mid < n - 1 and arr[mid] < arr[mid + 1]:
            left = mid + 1
        else:
            right = mid - 1

    return -1


if __name__ == "__main__":
    test_arrays = [
        [1, 3, 5, 7, 9, 8, 6, 4, 2],
        [10, 20, 30, 40, 50],
        [50, 40, 30, 20, 10],
        [1],
        [1, 2, 3, 4, 5, 4, 3],
        [1, 2, 3]
    ]

    for i, arr in enumerate(test_arrays, 1):
        peak_index = find_peak_element(arr)
        print(f"Тест {i}: массив {arr}")
        print(f"Пик находится по индексу: {peak_index} (значение: {arr[peak_index]})")
        print("-" * 50)
