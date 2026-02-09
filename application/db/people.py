"""Module for employee data access."""

__all__ = ["get_employees"]

import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# Вывод источника данных (с fallback для консолей без Unicode)
_SOURCE_LABELS = ("📊 БД", "📄 JSON", "🧪 Тест")
_SOURCE_LABELS_ASCII = ("[БД]", "[JSON]", "[Тест]")


def _print_source(index: int) -> None:
    try:
        print(_SOURCE_LABELS[index])
    except UnicodeEncodeError:
        print(_SOURCE_LABELS_ASCII[index])

# Минимальные тестовые данные при отсутствии JSON и БД
_FALLBACK_EMPLOYEES = [
    {"id": 0, "full_name": "Тестовый Сотрудник", "position": "Должность", "base_salary": 0, "is_active": True},
]


def _get_json_path() -> Path:
    """Путь к файлу employees.json."""
    return Path(__file__).resolve().parent.parent.parent / "data" / "employees.json"


def _try_load_from_db() -> list[dict[str, Any]] | None:
    """
    Опционально загрузить сотрудников из БД.
    Весь код работы с БД изолирован; при отсутствии sqlalchemy/asyncpg не импортируется.
    """
    try:
        from database.session import SessionLocal
        from database.models import Employee

        if SessionLocal is None or Employee is None:
            return None

        from sqlalchemy import select

        db = SessionLocal()
        try:
            result = db.execute(select(Employee).where(Employee.is_active == True))
            rows = result.scalars().all()
            return [_employee_row_to_dict(row) for row in rows]
        finally:
            db.close()
    except ImportError as e:
        logger.debug("БД не используется: отсутствуют зависимости (%s)", e)
        return None
    except Exception as e:
        logger.warning("БД недоступна, используем другой источник: %s", e)
        return None


def _employee_row_to_dict(row: Any) -> dict[str, Any]:
    """Привести строку БД к формату, совместимому с JSON."""
    return {
        "id": getattr(row, "id", None),
        "employee_code": getattr(row, "employee_code", ""),
        "full_name": getattr(row, "full_name", ""),
        "first_name": getattr(row, "first_name", ""),
        "last_name": getattr(row, "last_name", ""),
        "middle_name": getattr(row, "middle_name"),
        "birth_date": _date_to_str(getattr(row, "birth_date", None)),
        "hire_date": _date_to_str(getattr(row, "hire_date", None)),
        "department_id": getattr(row, "department_id", None),
        "department": "",
        "position": getattr(row, "position", ""),
        "tariff_grade": getattr(row, "tariff_grade", 1),
        "coefficient": float(getattr(row, "coefficient", 1.0)),
        "base_salary": float(getattr(row, "base_salary", 0)),
        "tax_deduction": float(getattr(row, "tax_deduction", 0)),
        "special_conditions": getattr(row, "special_conditions", None),
        "is_active": getattr(row, "is_active", True),
    }


def _date_to_str(value: Any) -> str | None:
    """Преобразовать date/datetime в строку YYYY-MM-DD."""
    if value is None:
        return None
    if hasattr(value, "isoformat"):
        return value.isoformat()[:10]
    return str(value)[:10]


def _load_from_json() -> list[dict[str, Any]] | None:
    """Загрузить сотрудников из JSON. При ошибке вернуть None."""
    path = _get_json_path()
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        employees = data.get("employees", [])
        return [e for e in employees if e.get("is_active", True)]
    except FileNotFoundError:
        logger.debug("Файл не найден: %s", path)
        return None
    except json.JSONDecodeError as e:
        logger.warning("Ошибка чтения JSON: %s", e)
        return None


def get_employees(use_db_if_available: bool = True) -> list[dict[str, Any]]:
    """
    Умная функция получения сотрудников.

    Логика:
    1. При use_db_if_available=True проверяется доступность БД (настройки, подключение).
    2. Если БД доступна и разрешена — данные берутся из БД.
    3. Иначе читаются из JSON.
    4. Если JSON недоступен — возвращаются тестовые данные.
    5. Всегда выводится источник данных (📊 БД / 📄 JSON / 🧪 Тест).

    Проект работает без установки sqlalchemy/asyncpg; БД — опциональное дополнение.

    Args:
        use_db_if_available: использовать БД, если она доступна.

    Returns:
        Список словарей сотрудников в едином формате из любого источника.
    """
    logger.info("Вызов get_employees()")

    # 1–2. Пробуем БД, если разрешено
    if use_db_if_available:
        from_db = _try_load_from_db()
        if from_db is not None and len(from_db) > 0:
            _print_source(0)
            logger.info("Загружено %s сотрудников из БД", len(from_db))
            return from_db

    # 3–4. JSON, затем тест
    from_json = _load_from_json()
    if from_json is not None and len(from_json) > 0:
        _print_source(1)
        logger.info("Загружено %s сотрудников из файла", len(from_json))
        return from_json

    # 5. Fallback
    _print_source(2)
    logger.warning("Используются тестовые данные (JSON и БД недоступны)")
    return list(_FALLBACK_EMPLOYEES)
