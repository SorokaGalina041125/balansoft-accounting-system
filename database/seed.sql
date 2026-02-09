-- Заполнение balansoft_db через raw SQL (альтернатива ORM seed.py)
-- Выполнить: psql -U user -d balansoft_db -f database/seed.sql
-- Таблицы departments и employees должны существовать:
--   alembic upgrade head  или  python -c "from database.seed import create_tables; create_tables()"

BEGIN;

-- Отделы
INSERT INTO departments (id, name, code) VALUES
(1, 'Руководство', 'MGMT'),
(2, 'Бухгалтерия', 'ACC'),
(3, 'IT-отдел', 'IT'),
(4, 'Отдел кадров', 'HR'),
(5, 'Административный', 'ADM')
ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name, code = EXCLUDED.code;

-- Сотрудники (3 примера; полный список — через python -m database.seed)
INSERT INTO employees (id, employee_code, full_name, first_name, last_name, middle_name, birth_date, hire_date, department_id, position, tariff_grade, coefficient, base_salary, tax_deduction, special_conditions, is_active) VALUES
(1, 'MGMT-001', 'Царевич Елисей Александрович', 'Елисей', 'Царевич', 'Александрович', '1985-03-18', '2020-01-15', 1, 'Генеральный директор', 6, 3.5, 140000, 0, NULL, true),
(2, 'ACC-001', 'Царевна Лебедь Владимировна', 'Лебедь', 'Царевна', 'Владимировна', '1990-07-22', '2020-03-10', 2, 'Главный бухгалтер', 5, 2.8, 115000, 1400, NULL, true),
(3, 'ACC-002', 'Баба Яга Кощеевна', 'Яга', 'Баба', 'Кощеевна', '1975-11-30', '2021-05-20', 2, 'Бухгалтер по расчету зарплаты', 4, 2.0, 80000, 2800, '{"type": "executive_proceedings", "deduction_percent": 30}', true)
ON CONFLICT (id) DO UPDATE SET full_name = EXCLUDED.full_name, base_salary = EXCLUDED.base_salary, tax_deduction = EXCLUDED.tax_deduction, special_conditions = EXCLUDED.special_conditions;

COMMIT;
