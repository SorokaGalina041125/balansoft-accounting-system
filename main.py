"""Balansoft: Основной модуль для запуска."""

import datetime
from application.salary import calculate_salary
from application.db.people import get_employees


if __name__ == "__main__":
    print("=== Balansoft: Система расчета зарплаты ===")
    print(f"Дата: {datetime.date.today()}")

    employees = get_employees()
    print(f"\nПолучено сотрудников: {len(employees)}")
    for i, emp in enumerate(employees, 1):
        print(f"{i}. {emp.get('full_name', 'N/A')} - {emp.get('position', 'N/A')}")

    salary_data = calculate_salary()
    print(f"\nРасчет зарплаты выполнен для: {salary_data.get('employee_name', 'N/A')}")
    print(f"К выплате: {salary_data.get('net_salary', 0):,.0f} руб.".replace(",", " "))
