# Auth Service

Микросервис аутентификации и авторизации. Часть приложения **Task Manager**.

## Задача сервиса

Отвечает за регистрацию пользователей, аутентификацию по email/паролю и выдачу JWT токенов. Все остальные сервисы приложения используют токены, выданные этим сервисом.

## Логика работы

1. Пользователь регистрируется через `POST /register`
2. Пользователь входит через `POST /login` — получает `access_token` (15 мин) и `refresh_token` (30 дней)
3. `access_token` передаётся в заголовке `Authorization: Bearer <token>` при запросах к любому сервису
4. При истечении `access_token` используется `POST /refresh` для получения нового
5. При `POST /logout` токен добавляется в Redis blacklist — становится недействительным немедленно

## Модели БД

**users**: `id`, `email`, `hashed_password`

**login_history**: `id`, `user_id`, `user_agent`, `logged_at`

## API эндпоинты

| Метод | URL | Описание | Авторизация |
|-------|-----|----------|-------------|
| POST | `/register` | Регистрация нового пользователя | Нет |
| POST | `/login` | Вход, получение JWT токенов | Нет |
| POST | `/refresh` | Обновление access токена | Нет |
| PUT | `/user/update` | Изменение email или пароля | Bearer token |
| GET | `/user/history` | История входов | Bearer token |
| POST | `/logout` | Выход, инвалидация токена в Redis | Bearer token |

## Запуск

### 1. Создай .env
```bash
cp .env.example .env
```

### 2. Запусти БД и Redis
```bash
docker-compose up -d
```

### 3. Установи зависимости и запусти
```bash
uv venv --python 3.12
.venv\Scripts\activate
uv pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Swagger UI: http://localhost:8000/docs

## Важно
Значение `JWT_SECRET_KEY` в `.env` должно совпадать с `JWT_SECRET_KEY` в Tasks Service.
