class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def lecturer_course_evaluation(self, lecturer, course, evaluation):
        if evaluation not in range(1, 11):
            return 'Оценка должна находиться в диапазоне от 1 до 10'
        if isinstance(lecturer,
                      Lecturer) and course in self.courses_in_progress and course in lecturer.courses_attached:
            if course in lecturer.evaluations:
                lecturer.evaluations[course] += [evaluation]
            else:
                lecturer.evaluations[course] = [evaluation]
        else:
            return 'Ошибка'

    def get_avg_grade(self, course_param=None):
        sum_grades = 0
        count_grades = 0
        for course, list_grade in self.grades.items():
            if course_param is None or course == course_param:
                for grade in list_grade:
                    count_grades += 1
                    sum_grades += grade
        if count_grades == 0:
            return 0
        return sum_grades / count_grades

    def __eq__(self, student):
        return self.get_avg_grade() == student.get_avg_grade()

    def __str__(self):
        return (f"Имя: {self.name}\n"
                f"Фамилия: {self.surname}\n"
                f"Средняя оценка за домашние задания: {self.get_avg_grade()}\n"
                f"Курсы в процессе изучения: {', '.join(course for course in self.courses_in_progress)}\n"
                f"Завершенные курсы: {', '.join(course for course in self.finished_courses)}")


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.evaluations = {}

    def get_avg_evaluation(self, course_param=None):
        sum_evaluations = 0
        count_evaluations = 0
        for course, list_evaluation in self.evaluations.items():
            if course_param is None or course == course_param:
                for evaluation in list_evaluation:
                    count_evaluations += 1
                    sum_evaluations += evaluation
        if count_evaluations == 0:
            return 0
        return sum_evaluations / count_evaluations

    def __eq__(self, lecturer):
        return self.get_avg_evaluation() == lecturer.get_avg_evaluation()

    def __str__(self):
        return f"Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за лекции: {self.get_avg_evaluation()}"


class Reviewer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)

    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        return f"Имя: {self.name}\nФамилия: {self.surname}"


def avg_grade_for_all_students(list_students, course_param):
    if len(list_students) == 0:
        return 'Ошибка. Студенты не указаны'

    sum_grade = 0
    for student in list_students:
        sum_grade += student.get_avg_grade(course_param)

    return sum_grade / len(list_students)


def avg_evaluation_for_all_lecturers(list_lecturers, course_param):
    if len(list_lecturers) == 0:
        return 'Ошибка. Лекторы не указаны'

    sum_evaluation = 0
    for lecturer in list_lecturers:
        sum_evaluation += lecturer.get_avg_evaluation(course_param)

    return sum_evaluation / len(list_lecturers)


# Создаем экземпляры классов(студенты, лекторы, эксперты)
student_one = Student('Ilya', 'Pokrovskiy', 'male')
student_two = Student('Ivan', 'Ivanov', 'male')

lecturer_one = Lecturer('Sergey', 'Sergeev')
lecturer_two = Lecturer('Dmitriy', 'Yan')

reviewer_one = Reviewer('Petr', 'Petrov')
reviewer_two = Reviewer('Vladimir', 'Lenin')

# Заполняем информацию о курсах студентов, лекторов, экспертов
student_one.courses_in_progress += ['Python', 'SQL', 'Js']
student_one.finished_courses += ['HTML', 'CSS']
student_two.courses_in_progress += ['Python', 'SQL', 'Js']

lecturer_one.courses_attached += ['SQL', 'Js']
lecturer_two.courses_attached += ['Python', 'SQL']

reviewer_one.courses_attached += ['Python', 'SQL', 'Js']
reviewer_two.courses_attached += ['Python', 'SQL']

# Эксперты выставляют оценки студентам
reviewer_one.rate_hw(student_one, 'Python', 8)
reviewer_one.rate_hw(student_one, 'SQL', 6)
reviewer_one.rate_hw(student_one, 'Js', 5)

reviewer_one.rate_hw(student_two, 'Python', 4)
reviewer_one.rate_hw(student_two, 'SQL', 7)
reviewer_one.rate_hw(student_two, 'Js', 10)

reviewer_two.rate_hw(student_one, 'Python', 6)
reviewer_two.rate_hw(student_one, 'SQL', 8)

reviewer_two.rate_hw(student_two, 'Python', 5)
reviewer_two.rate_hw(student_two, 'SQL', 4)

# Студенты дают оценку лекторам
student_one.lecturer_course_evaluation(lecturer_one, 'SQL', 10)
student_one.lecturer_course_evaluation(lecturer_one, 'Js', 8)
student_one.lecturer_course_evaluation(lecturer_two, 'Python', 7)
student_one.lecturer_course_evaluation(lecturer_two, 'SQL', 6)

student_two.lecturer_course_evaluation(lecturer_one, 'SQL', 6)
student_two.lecturer_course_evaluation(lecturer_one, 'Js', 5)
student_two.lecturer_course_evaluation(lecturer_two, 'Python', 3)
student_two.lecturer_course_evaluation(lecturer_two, 'SQL', 10)


# выводим информацию о студентах, лекторах, экспертах
print(f"Студент\n{student_one}\n")
print(f"Студент\n{student_two}\n")

print(f"Лектор\n{lecturer_one}\n")
print(f"Лектор\n{lecturer_two}\n")

print(f"Эксперт\n{reviewer_one}\n")
print(f"Эксперт\n{reviewer_two}\n")

course_example = 'Python'
print(f"Средняя оценка за домашние задания по всем студентам в рамках курса {course_example}: {avg_grade_for_all_students([student_one, student_two], course_example)}")
print(f"Средняя оценка за лекции всех лекторов в рамках курса {course_example}: {avg_evaluation_for_all_lecturers([lecturer_one, lecturer_two], course_example)}")
