"""Тесты для бизнес-логики и обработки списков."""

import pytest
from lab.models import Student
from lab.processing import (
    add_student, remove_student, update_grades,
    sort_students, filter_students, get_statistics, get_top_n
)
from lab.errors import DuplicateError, NotFoundError, ValidationError

def test_add_student(sample_students):
    """Тест добавления нового студента."""
    new_student = Student(id=4, name="Новый", grades=[100])
    add_student(sample_students, new_student)
    assert len(sample_students) == 4
    assert sample_students[-1].id == 4

def test_add_duplicate_student(sample_students):
    """Тест ошибки при добавлении дубликата."""
    dup_student = Student(id=1, name="Дубль", grades=[])
    with pytest.raises(DuplicateError):
        add_student(sample_students, dup_student)

def test_remove_student(sample_students):
    """Тест успешного удаления студента."""
    remove_student(sample_students, 1)
    assert len(sample_students) == 2
    assert all(s.id != 1 for s in sample_students)

def test_remove_not_found(sample_students):
    """Тест ошибки удаления несуществующего студента."""
    with pytest.raises(NotFoundError):
        remove_student(sample_students, 99)

def test_update_grades(sample_students):
    """Тест обновления оценок."""
    update_grades(sample_students, 2, [10, 20])
    assert sample_students[1].grades == [10, 20]

def test_sort_students_by_avg(sample_students):
    """Тест сортировки по среднему баллу."""
    sorted_list = sort_students(sample_students, 'avg')
    assert sorted_list[0].id == 1
    assert sorted_list[1].id == 2
    assert sorted_list[2].id == 3

def test_sort_students_invalid_key(sample_students):
    """Тест ошибки при неверном ключе сортировки."""
    with pytest.raises(ValidationError):
        sort_students(sample_students, 'invalid')

def test_filter_students(sample_students):
    """Тест фильтрации студентов по минимальному среднему баллу."""
    filtered = filter_students(sample_students, 70.0)
    assert len(filtered) == 1
    assert filtered[0].id == 1

def test_get_statistics(sample_students):
    """Тест расчета статистики группы."""
    stats = get_statistics(sample_students)
    assert stats['count'] == 3
    assert stats['best'].id == 1
    assert stats['worst'].id == 3
    assert 73.0 < stats['overall_avg'] < 75.0

def test_get_top_n(sample_students):
    """Тест получения топа студентов."""
    top = get_top_n(sample_students, 1)
    assert len(top) == 1
    assert top[0].id == 1