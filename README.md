# Проектная работа 6 спринта, команда 19

https://github.com/cmrd-a/Auth_sprint_1

## Проект "Фильмотека"
Состоит из:
 - ETL. Перегоняет данные из PostgreSQL в ElasticSearch.
 - Админка для создания, изменения и удаления вышеобозначенных объектов.
 - API для поиска информации о фильмах, жанрах и актёрах.
 - Сервис авторизации. Позволяет пользователю создать и пользоваться своей учётной записью, администратору - управлять правами пользователей.

### Запуск сервисов:
 1. `cp .env.example .env`
 2. `cp auth.env.example auth.env`
 3. `make prod_up`

API доступно по адресу: http://localhost/api/openapi.

А админка по http://localhost/admin/. Логин и пароль 'admin'.

### Запуск тестов:
 1. `cp tests/functional/.env.example tests/functional/.env`
 2. `make tests_up`

# Auth. Система авторизации
`alembic revision -m "init tables"`
`alembic upgrade head`
http://localhost/auth/docs

### Команды для разработки:
 - `make dev_up` - поднять только БД с открытыми портами.
 - `make black` - отформатировать код.

---
@cmrd-a - тимлид

@nu-kotov - разработчик