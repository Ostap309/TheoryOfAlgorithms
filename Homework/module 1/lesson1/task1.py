# Напишите программу которая определяет
# является ли паросочетание устойчивым
# Вход – таблицы предпочтений и паросочетания.
# Выход – ответ: Устойчивое или Неустойчивое.


# Создаем словарь отношений R со следующим смыслом:
# Ключ предпочел бы какое-либо из своих Значений текущему паросочетанию
# * - текущее паросочетание
def make_relations(rows: int, columns: int) -> dict:
    relations = {}
    for _ in range(rows):
        row = input().split()

        relations[row[0]] = []
        i = 1
        while i < columns + 1 and row[i][0] != "*":
            relations[row[0]].append(row[i])
            i += 1

    return relations


# Вводим размерность (n организаций и m работников)
n, m = map(int, input().split())

# Ищем отношения R в таблице организаций n x m и таблице работников m x n
org_relations, emp_relations = make_relations(n, m), make_relations(m, n)

for org in org_relations:

    # Организация org предпочитает работников emp
    for emp in org_relations[org]:

        # Предпочитает ли emp организацию org?
        if org in emp_relations[emp]:
            print("Неустойчивое")
            quit()

print("Устойчивое")
