"""Иерархия пользовательских исключений приложения."""

class AppError(Exception):
    """Базовое исключение приложения."""
    pass

class ValidationError(AppError):
    """Ошибка валидации данных."""
    pass

class FileError(AppError):
    """Ошибка при работе с файлами."""
    pass

class NotFoundError(AppError):
    """Сущность не найдена."""
    pass

class DuplicateError(AppError):
    """Сущность с таким идентификатором уже существует."""
    pass
