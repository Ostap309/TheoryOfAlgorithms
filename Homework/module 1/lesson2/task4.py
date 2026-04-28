# Покажите, что всегда существует устойчивое распределение студентов по больницам,
# и приведите алгоритм поиска такого распределения

# Объявление класса Госпиталь
class Hospital:
    def __init__(self, name, vacancy, preferences):
        self.name: str = name
        self.preferences: list[str] = preferences
        self.vacancy: int = int(vacancy)
        self.current_students: list = []  # тип list[Student]

    def is_full(self) -> bool:
        return self.vacancy == 0

    # Госпиталь предлагает место самому предпочтительному студенту из своего списка
    # Примечание: при вызове метода suggest(), должно гарантироваться наличие вакансии в Госпитале!
    def suggest(self):
        # Самый предпочтительный Студент
        next_preferred_name = self.preferences.pop(0)
        s: Student = next((student for student in students if student.name == next_preferred_name), None)

        # Студента делает выбор по Гейлу-Шепли:

        # Студентов не осталось (невозможная ситуация)
        if not s:
            print("Если видите эту строчку, то что-то пошло не так")
            return

        # Студент не числится в другом Госпитале
        if not s.current_hospital:
            # Образуется связь h <-> s
            s.current_hospital = self
            self.current_students.append(s)
            self.vacancy -= 1

        # Студент числился в другом Госпитале, но предпочел текущий Госпиталь (он же self)
        elif s.prefer(self):
            # Рушится связь h' <-> s
            old_hospital: Hospital = s.current_hospital
            old_hospital.current_students.remove(s)
            old_hospital.vacancy += 1

            # Создается связь h <-> s
            s.current_hospital = self
            self.current_students.append(s)
            self.vacancy -= 1

            # h' делает предложение следующему студенту из своего списка
            old_hospital.suggest()

        # В противном случае Студент остается на своем месте

    def __str__(self) -> str:
        result_string = self.name
        for student in self.current_students:
            result_string += f"\n\t* {student.name}"

        return result_string


# Объявление класса Студент
class Student:
    def __init__(self, name, preferences):
        self.name: str = name
        self.preferences: list[str] = preferences
        self.current_hospital: Hospital = None

    # Студент предпочитает новый Госпиталь, если он встречается в его списке раньше текущего
    def prefer(self, hospital: Hospital) -> bool:
        # Сравнение ведется по индексам в списке предпочтений
        if self.preferences.index(hospital.name) < self.preferences.index(self.current_hospital.name):
            return True

        return False


# Список Госпиталей
hospitals: list[Hospital] = []
# Список Студентов
students: list[Student] = []

# Ввод данных по Гостиницам
input_line = input().split()
while input_line:
    hospitals.append(Hospital(input_line[0], input_line[1], input_line[2:]))
    input_line = input().split()
# Ввод данных по Студентам
input_line = input().split()
while input_line:
    students.append(Student(input_line[0], input_line[1:]))
    input_line = input().split()

# Алгоритм
for h in hospitals:
    while not h.is_full():
        h.suggest()

# Вывод
for h in hospitals:
    print(h)
