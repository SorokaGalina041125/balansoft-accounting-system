# Схема БД Balansoft

## Таблицы (опционально)

### employees

| Поле               | Тип          | Описание                      |
|--------------------|--------------|-------------------------------|
| id                 | INTEGER      | PK                            |
| employee_code      | VARCHAR(20)  | Уникальный код                |
| full_name          | VARCHAR(200) | ФИО                           |
| base_salary        | FLOAT        | Оклад                         |
| tariff_grade       | INTEGER      | Разряд (1-6)                  |
| tax_deduction      | FLOAT        | Налоговый вычет               |
| special_conditions | JSON         | Особые условия (ИП, алименты) |

### departments

| Поле | Тип          | Описание |
|------|--------------|----------|
| id   | INTEGER      | PK       |
| name | VARCHAR(100) | Название |
| code | VARCHAR(10)  | Код      |

## PostgreSQL 18

Для работы с БД создать `.env` с `DATABASE_URL`.
