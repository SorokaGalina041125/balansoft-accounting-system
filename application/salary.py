"""Module for salary calculation."""

__all__ = ["calculate_salary"]

import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


def _get_data_path() -> Path:
    """Get path to employees JSON file."""
    return Path(__file__).resolve().parent.parent / "data" / "employees.json"


def _load_employee_by_id(employee_id: int) -> dict[str, Any] | None:
    """Load employee by ID from JSON."""
    data_path = _get_data_path()
    try:
        with open(data_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for emp in data.get("employees", []):
            if emp.get("id") == employee_id:
                return emp
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return None


def calculate_salary(employee_id: int = 3) -> dict[str, Any]:
    """
    Calculate salary for an employee.

    By default calculates for Баба Яга (id=3) with executive proceedings.
    Performs real calculation: NDFL 13%, tax deduction, special conditions.

    Args:
        employee_id: ID of employee to calculate (default: 3 - Баба Яга).

    Returns:
        Dict with employee_name, base_salary, ndfl, special_deduction, net_salary.
    """
    logger.info("Вызов calculate_salary()")

    from utils.salary_calculator import calculate_employee_salary

    employee = _load_employee_by_id(employee_id)
    if not employee:
        logger.warning(f"Сотрудник с id={employee_id} не найден")
        return {"employee_name": "Не найден", "net_salary": 0}

    result = calculate_employee_salary(employee)

    logger.info(f"Расчет для: {result['employee_name']}")
    logger.info(f"Оклад: {result['base_salary']:,} руб.".replace(",", " "))
    logger.info(f"НДФЛ: {result['ndfl']:,} руб.".replace(",", " "))

    if result["special_deduction"] > 0:
        cond_type = (result.get("special_conditions") or {}).get("type", "unknown")
        label = "ИП" if cond_type == "executive_proceedings" else "Алименты"
        logger.info(f"Удержание ({label}): {result['special_deduction']:,} руб.".replace(",", " "))

    logger.info(f"К выплате: {result['net_salary']:,} руб.".replace(",", " "))

    return result
