import numpy as np


def hungarian_maximize(matrix):
    """
    Ручная реализация Венгерского алгоритма для максимизации суммы назначений.

    Параметры:
    matrix (np.ndarray): входная матрица (n x n)

    Возвращает:
    np.ndarray: матрица назначений (1 — элемент выбран, 0 — не выбран)
    """
    # Шаг 0: преобразуем задачу максимизации в минимизацию
    cost_matrix = -matrix
    n = cost_matrix.shape[0]

    # Создаём рабочую копию матрицы
    work_matrix = cost_matrix.copy()

    # Шаг 1: вычитаем минимум в каждой строке
    for i in range(n):
        min_val = np.min(work_matrix[i, :])
        work_matrix[i, :] -= min_val

    # Шаг 2: вычитаем минимум в каждом столбце
    for j in range(n):
        min_val = np.min(work_matrix[:, j])
        work_matrix[:, j] -= min_val

    while True:
        # Шаг 3: находим минимальное покрытие нулей
        row_cover = np.zeros(n, dtype=bool)  # строки, покрытые линиями
        col_cover = np.zeros(n, dtype=bool)  # столбцы, покрытые линиями
        assignment = np.zeros((n, n), dtype=int)  # матрица назначений

        # Находим все нули и пытаемся сделать назначения
        for i in range(n):
            for j in range(n):
                if work_matrix[i, j] == 0 and not row_cover[i] and not col_cover[j]:
                    assignment[i, j] = 1
                    row_cover[i] = True
                    col_cover[j] = True

        # Сбрасываем покрытия для дальнейшего анализа
        row_cover[:] = False
        col_cover[:] = False

        # Помечаем строки без назначений
        marked_rows = np.where(~np.any(assignment, axis=1))[0]
        row_cover[marked_rows] = True

        # Строим минимальное покрытие
        changed = True
        while changed:
            changed = False
            # Помечаем столбцы с нулями в помеченных строках
            for i in np.where(row_cover)[0]:
                for j in range(n):
                    if work_matrix[i, j] == 0 and not col_cover[j]:
                        col_cover[j] = True
                        changed = True
            # Помечаем строки с назначениями в помеченных столбцах
            for j in np.where(col_cover)[0]:
                for i in range(n):
                    if assignment[i, j] == 1 and not row_cover[i]:
                        row_cover[i] = True
                        changed = True

        covered_rows = np.sum(row_cover)
        covered_cols = np.sum(col_cover)

        if covered_rows + covered_cols == n:
            # Все нули покрыты, назначения оптимальны
            break

        # Шаг 4: модифицируем матрицу
        # Находим минимальный непокрытый элемент
        min_uncovered = np.inf
        for i in range(n):
            if not row_cover[i]:
                for j in range(n):
                    if not col_cover[j]:
                        min_uncovered = min(min_uncovered, work_matrix[i, j])

        # Вычитаем минимум из всех непокрытых элементов
        for i in range(n):
            for j in range(n):
                if not row_cover[i] and not col_cover[j]:
                    work_matrix[i, j] -= min_uncovered
                elif row_cover[i] and col_cover[j]:
                    # Добавляем минимум к элементам на пересечении покрытых строк и столбцов
                    work_matrix[i, j] += min_uncovered

        print(work_matrix)

    return assignment


n = int(input())
ri = [float(input()) for i in range(n)]
matrix = np.empty((0, n))
for t in range(1, n + 1):
    row = np.floor(np.array(ri) ** t * 10) * 670
    matrix = np.vstack([matrix, row])
for row in hungarian_maximize(matrix):
    print(row)
