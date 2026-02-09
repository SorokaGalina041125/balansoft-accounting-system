"""Balansoft: Расширенный запуск с полным функционалом."""

import datetime
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)

from application.db.people import get_employees
from application.salary import calculate_salary
from utils.formatters import format_currency

try:
    from rich.console import Console
    from rich.table import Table

    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


def main() -> None:
    """Extended run with rich output."""
    if RICH_AVAILABLE:
        console = Console()
        console.print("\n[bold cyan]=== Balansoft: Система расчета зарплаты ===")
        console.print(f"[bold]Дата:[/bold] {datetime.date.today()}\n")

        employees = get_employees()
        table = Table(title="Сотрудники ООО Лукоморье")
        table.add_column("#", style="dim")
        table.add_column("ФИО", style="cyan")
        table.add_column("Должность", style="green")
        table.add_column("Оклад", justify="right")

        for i, emp in enumerate(employees, 1):
            table.add_row(
                str(i),
                emp.get("full_name", "N/A"),
                emp.get("position", "N/A"),
                format_currency(emp.get("base_salary", 0)),
            )
        console.print(table)

        salary_data = calculate_salary(employee_id=3)
        console.print(f"\n[bold]Расчет зарплаты (Баба Яга):[/bold]")
        console.print(f"  Оклад: {format_currency(salary_data.get('base_salary', 0))}")
        console.print(f"  НДФЛ: {format_currency(salary_data.get('ndfl', 0))}")
        console.print(f"  Удержание (ИП): {format_currency(salary_data.get('special_deduction', 0))}")
        console.print(f"  [bold green]К выплате: {format_currency(salary_data.get('net_salary', 0))}[/bold green]")
    else:
        print("=== Balansoft: Система расчета зарплаты ===")
        print(f"Дата: {datetime.date.today()}")
        employees = get_employees()
        print(f"\nПолучено сотрудников: {len(employees)}")
        for i, emp in enumerate(employees, 1):
            print(f"{i}. {emp.get('full_name')} - {emp.get('position')}")
        salary_data = calculate_salary()
        print(f"\nРасчет для: {salary_data.get('employee_name')}")
        print(f"К выплате: {salary_data.get('net_salary'):,.0f} руб.".replace(",", " "))


if __name__ == "__main__":
    main()
