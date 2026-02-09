"""SQLAlchemy models for Balansoft (optional DB layer)."""

from datetime import date
from typing import Optional

try:
    from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String, Boolean, JSON
    from sqlalchemy.orm import DeclarativeBase, relationship

    class Base(DeclarativeBase):
        """Base class for models."""

        pass

    class Department(Base):
        """Department model."""

        __tablename__ = "departments"

        id = Column(Integer, primary_key=True)
        name = Column(String(100), nullable=False)
        code = Column(String(10), nullable=False)

    class Employee(Base):
        """Employee model."""

        __tablename__ = "employees"

        id = Column(Integer, primary_key=True, autoincrement=True)
        employee_code = Column(String(20), unique=True)
        full_name = Column(String(200))
        first_name = Column(String(100))
        last_name = Column(String(100))
        middle_name = Column(String(100), nullable=True)
        birth_date = Column(Date)
        hire_date = Column(Date)
        department_id = Column(Integer, ForeignKey("departments.id"))
        position = Column(String(200))
        tariff_grade = Column(Integer)
        coefficient = Column(Float)
        base_salary = Column(Float)
        tax_deduction = Column(Float, default=0)
        special_conditions = Column(JSON, nullable=True)
        is_active = Column(Boolean, default=True)

except ImportError:
    Base = None
    Department = None
    Employee = None
