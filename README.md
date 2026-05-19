# Task Manager — Микросервисное приложение

Курсовая работа по предмету "Проектирование микросервисных систем".

Бэкенд приложение для управления задачами, построенное на микросервисной архитектуре.

## Архитектура

```
┌─────────────────────────────────────────────────────┐
│                      Клиент                          │
│                  (Swagger / curl)                    │
└──────────────┬──────────────────┬───────────────────┘
               │                  │
               ▼                  ▼
┌──────────────────┐   ┌──────────────────────┐
│   Auth Service   │   │    Tasks Service     │
│  localhost:8000  │   │   localhost:8001     │
│                  │   │                      │
│  - Регистрация   │   │  - Создание задач    │
│  - Логин / JWT   │   │  - Просмотр задач    │
│  - Refresh token │   │  - Обновление задач  │
│  - История входов│   │  - Удаление задач    │
│  - Logout        │   │  - Фильтрация        │
└────────┬─────────┘   └──────────┬───────────┘
         │                        │
         │   JWT_SECRET_KEY       │ валидирует JWT
         │   (общий секрет)  ◄────┘
         │
┌────────▼─────────┐   ┌──────────────────────┐
│   PostgreSQL     │   │      PostgreSQL       │
│   auth_db:5434   │   │    tasks_db:5435      │
└──────────────────┘   └──────────────────────┘
         │
┌────────▼─────────┐
│      Redis       │
│   localhost:6379 │
│  (token blacklist│
└──────────────────┘
```

## Сервисы

| Сервис | Порт | Описание |
|--------|------|----------|
| Auth Service | 8000 | Аутентификация, JWT токены |
| Tasks Service | 8001 | Управление задачами |
| auth_db (PostgreSQL) | 5434 | БД Auth Service |
| tasks_db (PostgreSQL) | 5435 | БД Tasks Service |
| Redis | 6379 | Blacklist токенов |

## Коммуникация между сервисами

Tasks Service валидирует JWT токены **локально** используя общий `JWT_SECRET_KEY`.
Это избавляет от необходимости HTTP-запроса к Auth Service при каждом обращении.

## Быстрый старт

### 1. Клонируй репозиторий

```bash
git clone <repo-url>
cd task_manager
```

### 2. Запусти все базы данных и Redis

```bash
docker-compose up -d
```

### 3. Запусти Auth Service (терминал 1)

```bash
cd auth_service
cp .env.example .env
uv venv --python 3.12
.venv\Scripts\activate
uv pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 4. Запусти Tasks Service (терминал 2)

```bash
cd tasks_service
cp .env.example .env
uv venv --python 3.12
.venv\Scripts\activate
uv pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

## Сценарий использования

```
1. POST http://localhost:8000/register   → регистрация
2. POST http://localhost:8000/login      → получить access_token
3. POST http://localhost:8001/api/v1/tasks/          → создать задачу
4. GET  http://localhost:8001/api/v1/tasks/           → список задач
5. GET  http://localhost:8001/api/v1/tasks/?task_status=todo  → фильтрация
6. PUT  http://localhost:8001/api/v1/tasks/{id}       → обновить задачу
7. DELETE http://localhost:8001/api/v1/tasks/{id}     → удалить задачу
8. POST http://localhost:8000/logout     → выход
```

Шаги 3-7 требуют заголовок: `Authorization: Bearer <access_token>`

## Swagger UI

- Auth Service: http://localhost:8000/docs
- Tasks Service: http://localhost:8001/docs

## Структура репозитория

```
task_manager/
├── auth_service/           ← Сервис аутентификации
│   ├── app/
│   │   ├── api/            ← HTTP эндпоинты
│   │   ├── core/           ← Конфиг, JWT, зависимости
│   │   ├── db/             ← БД, Redis
│   │   ├── models/         ← ORM модели
│   │   ├── schemas/        ← Pydantic схемы
│   │   ├── services/       ← Бизнес-логика
│   │   └── main.py
│   ├── docker-compose.yml
│   ├── .env.example
│   ├── requirements.txt
│   └── README.md
├── tasks_service/          ← Сервис задач
│   ├── app/
│   │   ├── api/            ← HTTP эндпоинты
│   │   ├── core/           ← Конфиг, JWT, зависимости
│   │   ├── db/             ← БД
│   │   ├── models/         ← ORM модели
│   │   ├── schemas/        ← Pydantic схемы
│   │   ├── services/       ← Бизнес-логика
│   │   └── main.py
│   ├── docker-compose.yml
│   ├── .env.example
│   ├── requirements.txt
│   └── README.md
└── docker-compose.yml      ← Общий, поднимает все БД сразу
```
