.PHONY: up down restart logs auth tasks install-auth install-tasks run-auth run-tasks

# Поднять все базы данных и Redis
up:
	docker-compose up -d

# Остановить все контейнеры
down:
	docker-compose down

# Перезапустить контейнеры
restart: down up

# Логи всех контейнеров
logs:
	docker-compose logs -f

# Установить зависимости Auth Service
install-auth:
	cd auth_service && uv venv --python 3.12 && .venv/Scripts/activate && uv pip install -r requirements.txt

# Установить зависимости Tasks Service
install-tasks:
	cd tasks_service && uv venv --python 3.12 && .venv/Scripts/activate && uv pip install -r requirements.txt

# Запустить Auth Service (порт 8000)
run-auth:
	cd auth_service && .venv/Scripts/activate && uvicorn app.main:app --reload --port 8000

# Запустить Tasks Service (порт 8001)
run-tasks:
	cd tasks_service && .venv/Scripts/activate && uvicorn app.main:app --reload --port 8001
