"""Модели данных приложения."""

from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Student:
    """Класс для хранения данных о студенте."""

    id: int
    name: str
    grades: List[Optional[int]]

    @property
    def average(self) -> float:
        """Возвращает средний балл студента по имеющимся оценкам."""
        valid_grades = [g for g in self.grades if g is not None]
        if not valid_grades:
            return 0.0
        return sum(valid_grades) / len(valid_grades)
