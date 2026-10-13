"""Фикстуры для тестирования."""

import pytest
from lab.models import Student

@pytest.fixture
def sample_students():
    """Возвращает базовый список студентов для тестов."""
    return [
        Student(id=1, name="Студент А", grades=[100, 90, None]),
        Student(id=2, name="Студент Б", grades=[50, 60, 70]),
        Student(id=3, name="Студент В", grades=[None, None])
    ]
