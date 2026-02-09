"""Seed script for balansoft_db — заполнение БД из data/employees.json."""

import json
from datetime import datetime
from pathlib import Path

from sqlalchemy import delete
from sqlalchemy.orm import Session
from database.models import Base, Department, Employee
from database.session import engine, SessionLocal


def _get_json_path() -> Path:
    """Путь к employees.json."""
    return Path(__file__).resolve().parent.parent / "data" / "employees.json"


def _parse_date(s: str | None) -> datetime | None:
    """Строку YYYY-MM-DD в date."""
    if not s:
        return None
    try:
        return datetime.strptime(s[:10], "%Y-%m-%d")
    except ValueError:
        return None


def load_data() -> dict:
    """Загрузить данные из JSON."""
    path = _get_json_path()
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def seed_departments(db: Session, data: dict) -> None:
    """Заполнить таблицу departments."""
    for dept in data.get("departments", []):
        obj = Department(
            id=dept["id"],
            name=dept["name"],
            code=dept["code"],
        )
        db.merge(obj)
    db.commit()


def seed_employees(db: Session, data: dict) -> int:
    """Заполнить таблицу employees. Возвращает количество добавленных."""
    count = 0
    for emp in data.get("employees", []):
        obj = Employee(
            id=emp["id"],
            employee_code=emp["employee_code"],
            full_name=emp["full_name"],
            first_name=emp["first_name"],
            last_name=emp["last_name"],
            middle_name=emp.get("middle_name"),
            birth_date=_parse_date(emp.get("birth_date")),
            hire_date=_parse_date(emp.get("hire_date")),
            department_id=emp["department_id"],
            position=emp["position"],
            tariff_grade=emp["tariff_grade"],
            coefficient=float(emp["coefficient"]),
            base_salary=float(emp["base_salary"]),
            tax_deduction=float(emp.get("tax_deduction", 0)),
            special_conditions=emp.get("special_conditions"),
            is_active=emp.get("is_active", True),
        )
        db.merge(obj)
        count += 1
    db.commit()
    return count


def create_tables() -> None:
    """Создать таблицы (если не существуют)."""
    Base.metadata.create_all(bind=engine)


def run_seed(clear_existing: bool = False) -> None:
    """
    Заполнить БД данными из JSON.

    Args:
        clear_existing: если True — очистить таблицы перед вставкой.
    """
    if engine is None or SessionLocal is None:
        raise RuntimeError("SQLAlchemy не установлен. pip install sqlalchemy python-dotenv")

    create_tables()

    db = SessionLocal()
    try:
        if clear_existing:
            db.execute(delete(Employee))
            db.execute(delete(Department))
            db.commit()

        data = load_data()

        seed_departments(db, data)
        n = seed_employees(db, data)

        print(f"OK: добавлено {n} сотрудников, {len(data.get('departments', []))} отделов")
    finally:
        db.close()


if __name__ == "__main__":
    import sys

    clear = "--clear" in sys.argv
    run_seed(clear_existing=clear)
