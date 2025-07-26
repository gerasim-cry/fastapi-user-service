# FastAPI User Management Service

**Полноценное REST API-приложение на FastAPI** с авторизацией, регистрацией, логированием действий пользователей и CI/CD пайплайном на GitHub Actions. Хранение данных — PostgreSQL. Контейнеризация через Docker.

## Функциональность

- Регистрация и авторизация пользователей (JWT)
- CRUD-операции над пользователями
- Логирование действий пользователей
- PostgreSQL + SQLAlchemy + Alembic
- Контейнеризация через Docker
- CI/CD пайплайн через GitHub Actions
- Pytest и тест эндпоинтов
- Автоматическое создание схемы БД

## Технологии

| Компонент     | Используется                    |
|---------------|---------------------------------|
| Backend       | FastAPI, Pydantic               |
| Database      | PostgreSQL, SQLAlchemy, Alembic |
| Auth          | OAuth2 (JWT)                    |
| CI/CD         | GitHub Actions                  |
| Тесты         | Pytest                          |
| Контейнеризация | Docker, docker-compose        |

# Как запустить проект

## Клонируем репозиторий
git clone https://github.com/gerasim-cry/fastapi-user-service.git
cd fastapi-user-service

## Запускаем проект
docker-compose up --build

API будет доступно по адресу: http://localhost:8000

# Переменные окружения

DATABASE_URL=postgresql://user:password@db:5432/appdb
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Запуск тестов

## Запуск тестов в контейнере
docker-compose run --rm web pytest

## Локально (если установлен Python)
PYTHONPATH=. pytest



