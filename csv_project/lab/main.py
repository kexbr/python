"""Точка входа и консольный интерфейс приложения."""

import sys
from typing import List, Optional
from .models import Student
from .errors import AppError
from . import processing
from . import io_utils

def print_menu() -> None:
    """Выводит на экран пункты консольного меню."""
    print("\n--- Меню управления студентами ---")
    print("1. Загрузка из CSV")
    print("2. Сохранение в CSV")
    print("3. Показ всех студентов")
    print("4. Добавление студента")
    print("5. Удаление по id")
    print("6. Обновление оценок по id")
    print("7. Показ статистики по группе")
    print("8. Экспорт ТОП-N студентов в CSV по среднему баллу")
    print("9. Сортировка и показ результата")
    print("10. Фильтрация по минимальному среднему баллу")
    print("0. Выход")

def parse_grades_input(input_str: str) -> List[Optional[int]]:
    """Разбирает пользовательский ввод оценок."""
    grades: List[Optional[int]] = []
    for part in input_str.split():
        if part == '-':
            grades.append(None)
        else:
            val = int(part)
            if not (0 <= val <= 100):
                raise ValueError(f"Оценка {val} вне диапазона 0-100.")
            grades.append(val)
    return grades

def print_students_table(students: List[Student]) -> None:
    """Выводит список студентов в виде отформатированной таблицы."""
    if not students:
        print("Список пуст.")
        return
    
    max_grades = max((len(s.grades) for s in students), default=0)
    
    header = f"| {'ID':<4} | {'ФИО':<20} |"
    for i in range(max_grades):
        header += f" {'Оц.'+str(i+1):<5} |"
    header += f" {'Ср.балл':<8} |"
    
    border = "-" * len(header)
    print(border)
    print(header)
    print(border)
    
    for s in students:
        row = f"| {s.id:<4} | {s.name:<20} |"
        for i in range(max_grades):
            val = s.grades[i] if i < len(s.grades) else None
            val_str = str(val) if val is not None else "-"
            row += f" {val_str:<5} |"
        row += f" {s.average:<8.2f} |"
        print(row)
    print(border)

def run() -> None:
    """Основной цикл работы консольного приложения."""
    students: List[Student] = []
    while True:
        print_menu()
        choice = input("Выберите действие: ").strip()
        try:
            if choice == '1':
                filepath = input("Введите путь к файлу CSV (по умолчанию data/students.csv): ").strip() or "data/students.csv"
                has_header_input = input("Файл содержит заголовок? (y/n, по умолчанию y): ").strip().lower()
                has_header = has_header_input != 'n'
                students = io_utils.read_csv(filepath, has_header=has_header)
                print(f"Загружено студентов: {len(students)}")
            elif choice == '2':
                filepath = input("Введите путь для сохранения: ").strip()
                io_utils.write_csv(filepath, students)
                print("Данные успешно сохранены.")
            elif choice == '3':
                print_students_table(students)
            elif choice == '4':
                s_id = int(input("Введите ID (число): ").strip())
                name = input("Введите ФИО: ").strip()
                g_str = input("Введите оценки через пробел (используйте '-' для пропусков): ").strip()
                grades = parse_grades_input(g_str)
                processing.add_student(students, Student(id=s_id, name=name, grades=grades))
                print("Студент добавлен.")
            elif choice == '5':
                s_id = int(input("Введите ID для удаления: ").strip())
                processing.remove_student(students, s_id)
                print("Студент удален.")
            elif choice == '6':
                s_id = int(input("Введите ID для обновления оценок: ").strip())
                g_str = input("Введите новые оценки через пробел (используйте '-' для пропусков): ").strip()
                grades = parse_grades_input(g_str)
                processing.update_grades(students, s_id, grades)
                print("Оценки обновлены.")
            elif choice == '7':
                stats = processing.get_statistics(students)
                print(f"Всего студентов: {stats['count']}")
                print(f"Общий средний балл: {stats['overall_avg']:.2f}")
                if stats['best']:
                    print(f"Лучший студент: {stats['best'].name} ({stats['best'].average:.2f})")
                if stats['worst']:
                    print(f"Худший студент: {stats['worst'].name} ({stats['worst'].average:.2f})")
            elif choice == '8':
                n = int(input("Введите N: ").strip())
                filepath = input("Введите путь для экспорта: ").strip()
                top_students = processing.get_top_n(students, n)
                io_utils.export_top_n_csv(filepath, top_students)
                print("Экспорт завершен.")
            elif choice == '9':
                key = input("Введите ключ сортировки (avg, name, id): ").strip()
                sorted_students = processing.sort_students(students, key)
                print_students_table(sorted_students)
            elif choice == '10':
                min_avg = float(input("Введите минимальный средний балл: ").strip())
                filtered = processing.filter_students(students, min_avg)
                print_students_table(filtered)
            elif choice == '0':
                print("Завершение работы.")
                break
            else:
                print("Неизвестная команда.")
        except AppError as e:
            print(f"Ошибка выполнения: {e}")
        except ValueError as e:
            print(f"Ошибка ввода данных: некорректное число или формат ({e})")
        except Exception as e:
            print(f"Непредвиденная системная ошибка: {e}")

if __name__ == "__main__":
    run()