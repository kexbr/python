"""Тесты для проверки базовых сценариев консольного интерфейса."""

from lab.main import run

def test_cli_exit(monkeypatch, capsys):
    """Тест сценария немедленного выхода из приложения."""
    monkeypatch.setattr('builtins.input', lambda _: '0')
    run()
    captured = capsys.readouterr()
    assert "Завершение работы." in captured.out

def test_cli_add_and_show(monkeypatch, capsys):
    """Тест добавления студента через CLI и табличного отображения списка."""
    inputs = iter(["4", "99", "Студент Тест", "100 90 -", "3", "0"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    run()

    captured = capsys.readouterr()
    assert "Студент добавлен." in captured.out
    assert "| 99   | Студент Тест" in captured.out
    assert "95.00" in captured.out

def test_cli_load_and_filter(monkeypatch, capsys, tmp_path):
    """Тест загрузки CSV (с подтверждением заголовка) и фильтрации студентов."""
    file_path = tmp_path / "test.csv"
    file_path.write_text("id,name,grade\n1,Отличник,100\n2,Двоечник,20", encoding="utf-8")
    
    inputs = iter(["1", str(file_path), "y", "10", "50", "0"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    run()
    captured = capsys.readouterr()
    
    assert "Загружено студентов: 2" in captured.out
    
    output_after_filter = captured.out.split("Введите минимальный средний балл:")[-1]
    
    assert "Отличник" in output_after_filter
    assert "Двоечник" not in output_after_filter