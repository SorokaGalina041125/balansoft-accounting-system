"""Salary calculation logic."""

import logging
from typing import Any

logger = logging.getLogger(__name__)

NDFL_RATE = 0.13  # 13%


def calculate_ndfl(gross_salary: float, tax_deduction: float = 0) -> float:
    """Calculate NDFL (personal income tax) with deduction."""
    taxable = max(0, gross_salary - tax_deduction)
    return round(taxable * NDFL_RATE, 2)


def calculate_special_deduction(
    net_after_ndfl: float, special_conditions: dict | None
) -> float:
    """Calculate deduction for executive proceedings or alimony."""
    if not special_conditions:
        return 0.0

    percent = special_conditions.get("deduction_percent", 0)
    return round(net_after_ndfl * (percent / 100), 2)


def calculate_employee_salary(employee: dict[str, Any]) -> dict[str, Any]:
    """
    Calculate full salary for one employee.

    Args:
        employee: Employee data dict with base_salary, tax_deduction, special_conditions.

    Returns:
        Dict with gross, ndfl, special_deduction, net, and details.
    """
    base_salary = employee.get("base_salary", 0)
    tax_deduction = employee.get("tax_deduction", 0)
    special_conditions = employee.get("special_conditions")

    gross = base_salary
    ndfl = calculate_ndfl(gross, tax_deduction)
    net_after_ndfl = gross - ndfl
    special_deduction = calculate_special_deduction(net_after_ndfl, special_conditions)
    net = round(net_after_ndfl - special_deduction, 2)

    return {
        "employee_id": employee.get("id"),
        "employee_name": employee.get("full_name"),
        "base_salary": base_salary,
        "tax_deduction": tax_deduction,
        "ndfl": ndfl,
        "special_deduction": special_deduction,
        "special_conditions": special_conditions,
        "net_salary": net,
    }
