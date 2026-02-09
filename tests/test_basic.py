"""Basic tests for Balansoft."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from application.db.people import get_employees
from application.salary import calculate_salary


def test_get_employees() -> None:
    """Test get_employees returns 10 employees."""
    employees = get_employees()
    assert len(employees) == 10
    assert employees[0]["full_name"] == "Царевич Елисей Александрович"


def test_calculate_salary() -> None:
    """Test calculate_salary for Баба Яга (с налоговым вычетом 2800)."""
    result = calculate_salary(employee_id=3)
    assert result["employee_name"] == "Баба Яга Кощеевна"
    assert result["base_salary"] == 80000
    assert result["ndfl"] == 10036.0  # (80000 - 2800) * 0.13
    assert result["special_deduction"] == 20989.2  # 30% от суммы после НДФЛ
    assert result["net_salary"] == 48974.8
