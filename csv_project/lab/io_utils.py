"""Утилиты для работы с вводом-выводом и файлами CSV."""

import csv
import os
from typing import List, Optional
from .models import Student
from .errors import FileError, ValidationError, AppError, DuplicateError

def read_csv(filepath: str, has_header: bool = True) -> List[Student]:
    """Читает данные о студентах из CSV файла."""
    if not os.path.exists(filepath):
        raise FileError(f"Файл {filepath} не найден.")

    students = []
    seen_ids = set()
    try:
        with open(filepath, mode='r', encoding='utf-8', newline='') as f:
            reader = csv.reader(f)
            if has_header:
                next(reader, None)

            for row_idx, row in enumerate(reader, start=2 if has_header else 1):
                if not row:
                    continue
                if len(row) < 2:
                    raise ValidationError(f"Строка {row_idx}: недостаточно данных.")
                try:
                    student_id = int(row[0].strip())
                except ValueError:
                    raise ValidationError(f"Строка {row_idx}: некорректный ID.")
                
                if student_id in seen_ids:
                    raise DuplicateError(f"Строка {row_idx}: дубликат ID {student_id}.")
                seen_ids.add(student_id)

                name = row[1].strip()
                grades: List[Optional[int]] = []
                for g in row[2:]:
                    g_str = g.strip()
                    if not g_str:
                        grades.append(None)
                    else:
                        try:
                            val = int(g_str)
                        except ValueError:
                            raise ValidationError(f"Строка {row_idx}: нечисловая оценка.")
                        if not (0 <= val <= 100):
                            raise ValidationError(f"Строка {row_idx}: оценка вне диапазона 0-100.")
                        grades.append(val)
                students.append(Student(id=student_id, name=name, grades=grades))
    except AppError:
        raise
    except Exception as e:
        raise FileError(f"Непредвиденная ошибка при чтении файла: {e}")
    return students

def write_csv(filepath: str, students: List[Student], write_header: bool = True) -> None:
    """Сохраняет данные о студентах в CSV файл с выравниванием колонок."""
    max_grades = max((len(s.grades) for s in students), default=0)
    try:
        with open(filepath, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            if write_header:
                header = ['id', 'name'] + [f'grade{i+1}' for i in range(max_grades)]
                writer.writerow(header)
            for s in students:
                row = [s.id, s.name]
                padded_grades = s.grades + [None] * (max_grades - len(s.grades))
                row.extend(['' if g is None else str(g) for g in padded_grades])
                writer.writerow(row)
    except Exception as e:
        raise FileError(f"Ошибка при записи в файл: {e}")

def export_top_n_csv(filepath: str, students: List[Student]) -> None:
    """Экспортирует студентов в CSV со специфичными колонками."""
    try:
        with open(filepath, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'name', 'average', 'grades'])
            for s in students:
                grades_str = ' '.join(str(g) for g in s.grades if g is not None).strip()
                writer.writerow([s.id, s.name, f"{s.average:.2f}", grades_str])
    except Exception as e:
        raise FileError(f"Ошибка при экспорте файла: {e}")