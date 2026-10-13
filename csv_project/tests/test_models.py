"""Тесты для моделей данных."""

from lab.models import Student

def test_student_average_normal():
    """Тест расчета среднего балла при наличии оценок."""
    s = Student(id=1, name="Тест", grades=[80, 90, 100])
    assert s.average == 90.0

def test_student_average_with_none():
    """Тест расчета среднего балла с пропусками."""
    s = Student(id=1, name="Тест", grades=[100, None, 50])
    assert s.average == 75.0

def test_student_average_empty():
    """Тест расчета среднего балла без оценок."""
    s = Student(id=1, name="Тест", grades=[None, None])
    assert s.average == 0.0
