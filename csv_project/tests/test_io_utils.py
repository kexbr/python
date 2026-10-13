"""Тесты функций чтения и записи."""

import pytest
import os
from lab.io_utils import read_csv, write_csv, export_top_n_csv
from lab.models import Student
from lab.errors import ValidationError, FileError, DuplicateError

def test_read_write_roundtrip(tmp_path, sample_students):
    """Тест полного цикла записи и последующего чтения CSV."""
    file_path = tmp_path / "test_students.csv"
    write_csv(str(file_path), sample_students)
    assert os.path.exists(file_path)
    loaded = read_csv(str(file_path))
    assert len(loaded) == len(sample_students)
    assert loaded[0].name == sample_students[0].name
    assert loaded[0].grades == sample_students[0].grades

def test_read_invalid_file():
    """Тест чтения несуществующего файла."""
    with pytest.raises(FileError):
        read_csv("non_existent_file.csv")

def test_read_invalid_data(tmp_path):
    """Тест обработки некорректных данных в CSV."""
    file_path = tmp_path / "bad.csv"
    file_path.write_text("id,name,grade\n1,Test,not_a_number", encoding="utf-8")
    with pytest.raises(ValidationError):
        read_csv(str(file_path))

def test_read_duplicate_ids(tmp_path):
    """Тест выброса исключения при наличии дубликатов ID в CSV файле."""
    file_path = tmp_path / "dup.csv"
    file_path.write_text("id,name,grade\n1,Иван,100\n1,Петр,90", encoding="utf-8")
    with pytest.raises(DuplicateError):
        read_csv(str(file_path))

def test_read_no_header(tmp_path):
    """Тест чтения файла без заголовка."""
    file_path = tmp_path / "no_header.csv"
    file_path.write_text("1,Студент 1,100,90\n2,Студент 2,80,70", encoding="utf-8")
    loaded = read_csv(str(file_path), has_header=False)
    assert len(loaded) == 2
    assert loaded[0].id == 1
    assert loaded[1].id == 2

def test_export_top_n(tmp_path, sample_students):
    """Тест функции экспорта ТОП-N студентов."""
    file_path = tmp_path / "top.csv"
    export_top_n_csv(str(file_path), sample_students)
    content = file_path.read_text(encoding="utf-8").strip().split('\n')
    assert len(content) == 4
    assert "average" in content[0]