# Tasks Service

Микросервис управления задачами. Часть приложения **Task Manager**.

## Задача сервиса

Предоставляет CRUD API для управления задачами пользователей. Каждый пользователь видит и управляет только своими задачами. Аутентификация осуществляется через JWT токены, выданные Auth Service.

## Логика работы

1. Клиент получает JWT access токен от **Auth Service** (`POST /login`)
2. Все запросы к Tasks Service отправляются с заголовком `Authorization: Bearer <token>`
3. Tasks Service самостоятельно валидирует JWT (shared secret), извлекает `user_id`
4. Все операции с задачами привязаны к `user_id` из токена

## Модель задачи

| Поле | Тип | Описание |
|------|-----|----------|
| id | int | Уникальный идентификатор |
| title | string | Название задачи |
| description | string | Описание (опционально) |
| status | enum | `todo` / `in_progress` / `done` |
| priority | enum | `low` / `medium` / `high` |
| owner_id | int | ID пользователя из Auth Service |
| created_at | datetime | Дата создания |
| updated_at | datetime | Дата обновления |

## API эндпоинты

Все эндпоинты требуют заголовок `Authorization: Bearer <access_token>`

| Метод | URL | Описание |
|-------|-----|----------|
| POST | `/api/v1/tasks/` | Создать задачу |
| GET | `/api/v1/tasks/` | Список своих задач |
| GET | `/api/v1/tasks/{id}` | Получить задачу по ID |
| PUT | `/api/v1/tasks/{id}` | Обновить задачу |
| DELETE | `/api/v1/tasks/{id}` | Удалить задачу |

### Фильтрация списка задач

```
GET /api/v1/tasks/?task_status=todo
GET /api/v1/tasks/?priority=high
GET /api/v1/tasks/?task_status=in_progress&priority=medium
```

## Запуск

### 1. Убедись что Auth Service запущен на порту 8000

### 2. Создай .env

```bash
cp .env.example .env
# Убедись что JWT_SECRET_KEY совпадает с Auth Service
```

### 3. Запусти базу данных

```bash
docker-compose up -d
```

### 4. Установи зависимости и запусти

```bash
uv venv --python 3.12
.venv\Scripts\activate   # Windows
source .venv/bin/activate  # Mac/Linux

uv pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

Swagger UI: http://localhost:8001/docs

## Связь с Auth Service

Tasks Service валидирует JWT токены локально используя общий `JWT_SECRET_KEY`.
Оба сервиса должны иметь одинаковое значение `JWT_SECRET_KEY` в `.env`.
