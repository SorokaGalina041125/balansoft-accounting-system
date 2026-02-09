"""Initial schema: departments, employees

Revision ID: 001
Revises:
Create Date: 2025-02-09

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "departments",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("code", sa.String(10), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "employees",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("employee_code", sa.String(20), nullable=True),
        sa.Column("full_name", sa.String(200), nullable=True),
        sa.Column("first_name", sa.String(100), nullable=True),
        sa.Column("last_name", sa.String(100), nullable=True),
        sa.Column("middle_name", sa.String(100), nullable=True),
        sa.Column("birth_date", sa.Date(), nullable=True),
        sa.Column("hire_date", sa.Date(), nullable=True),
        sa.Column("department_id", sa.Integer(), nullable=True),
        sa.Column("position", sa.String(200), nullable=True),
        sa.Column("tariff_grade", sa.Integer(), nullable=True),
        sa.Column("coefficient", sa.Float(), nullable=True),
        sa.Column("base_salary", sa.Float(), nullable=True),
        sa.Column("tax_deduction", sa.Float(), nullable=True),
        sa.Column("special_conditions", sa.JSON(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(["department_id"], ["departments.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_employees_employee_code"),
        "employees",
        ["employee_code"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_employees_employee_code"), table_name="employees")
    op.drop_table("employees")
    op.drop_table("departments")
