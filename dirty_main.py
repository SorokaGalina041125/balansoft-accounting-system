"""
Необязательное задание: импорт через from package.module import *.

Внимание: использование import * не рекомендуется в production-коде.
"""

import datetime
from application.salary import *
from application.db.people import *


if __name__ == "__main__":
    print("=== Balansoft (dirty_main): import * ===")
    print(f"Дата: {datetime.date.today()}")

    employees = get_employees()
    print(f"\nПолучено сотрудников: {len(employees)}")

    salary_data = calculate_salary()
    print(f"Расчет для: {salary_data.get('employee_name', 'N/A')}")
