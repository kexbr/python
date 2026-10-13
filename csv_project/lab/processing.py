"""Функции для обработки данных и бизнес-логики."""

from typing import List, Optional, Dict, Any
from .models import Student
from .errors import DuplicateError, NotFoundError, ValidationError

def add_student(students: List[Student], student: Student) -> None:
    """Добавляет нового студента в список."""
    if any(s.id == student.id for s in students):
        raise DuplicateError(f"Студент с id {student.id} уже существует.")
    students.append(student)

def remove_student(students: List[Student], student_id: int) -> None:
    """Удаляет студента по id."""
    for i, student in enumerate(students):
        if student.id == student_id:
            students.pop(i)
            return
    raise NotFoundError(f"Студент с id {student_id} не найден.")

def update_grades(students: List[Student], student_id: int, grades: List[Optional[int]]) -> None:
    """Обновляет оценки студента по id."""
    for student in students:
        if student.id == student_id:
            student.grades = grades
            return
    raise NotFoundError(f"Студент с id {student_id} не найден.")

def sort_students(students: List[Student], key: str) -> List[Student]:
    """Сортирует список студентов по заданному ключу (avg, name, id)."""
    if key == 'avg':
        return sorted(students, key=lambda s: (-s.average, s.name))
    elif key == 'name':
        return sorted(students, key=lambda s: s.name)
    elif key == 'id':
        return sorted(students, key=lambda s: s.id)
    else:
        raise ValidationError(f"Неизвестный ключ сортировки: {key}")

def filter_students(students: List[Student], min_avg: float) -> List[Student]:
    """Фильтрует список студентов по минимальному среднему баллу."""
    return [s for s in students if s.average >= min_avg]

def get_statistics(students: List[Student]) -> Dict[str, Any]:
    """Рассчитывает групповую статистику по списку студентов."""
    count = len(students)
    if not count:
        return {"count": 0, "overall_avg": 0.0, "best": None, "worst": None}

    all_grades = [g for s in students for g in s.grades if g is not None]
    overall_avg = sum(all_grades) / len(all_grades) if all_grades else 0.0

    best = max(students, key=lambda s: s.average)
    worst = min(students, key=lambda s: s.average)

    return {
        "count": count,
        "overall_avg": overall_avg,
        "best": best,
        "worst": worst
    }

def get_top_n(students: List[Student], n: int) -> List[Student]:
    """Возвращает ТОП-N студентов по среднему баллу."""
    return sort_students(students, 'avg')[:n]