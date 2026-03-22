# Atomic Habits API

Backend for a habit tracker inspired by *Atomic Habits*. It exposes a REST API for creating and managing habits, with validation rules, optional Telegram reminders (Celery), and public habit listings.

![Python](https://img.shields.io/badge/python-3.13+-blue.svg)
![Django](https://img.shields.io/badge/django-5.2+-green.svg)
![Celery](https://img.shields.io/badge/celery--beat-enabled-orange.svg)
![Redis](https://img.shields.io/badge/redis-broker-red.svg)
[![Tests](https://github.com/AJLbN0H/atomic-habits-api/actions/workflows/tests.yml/badge.svg)](https://github.com/AJLbN0H/atomic-habits-api/actions/workflows/tests.yml)

## Features

- **Habits CRUD** — create, read, update, and delete habits (including “pleasant” habits and rewards).
- **Serializer validation** — e.g. cannot combine reward and associated pleasant habit; time cap; periodicity limits; `chat_id` format.
- **Reminders** — Celery Beat can run periodic tasks (e.g. Telegram notifications).
- **Public habits** — habits can be marked public for sharing.
- **Auth** — JWT via `djangorestframework-simplejwt`.

## Stack

| Layer        | Technology                          |
| ------------ | ----------------------------------- |
| API          | Django REST Framework               |
| DB           | PostgreSQL                          |
| Tasks        | Celery + django-celery-beat         |
| Broker/cache | Redis                               |
| Docs (optional) | drf-yasg (Swagger/OpenAPI)       |

## Project layout

- `habits/` — models, serializers, views, tasks, permissions.
- `users/` — custom user model and auth-related endpoints.
- `config/` — Django settings, URLs, Celery app.

## Quick start (Docker)

1. Clone the repo:

   ```bash
   git clone https://github.com/AJLbN0H/atomic-habits-api.git
   cd atomic-habits-api
   ```

2. Copy environment template and adjust secrets:

   ```bash
   cp .env.sample .env
   ```

   Set at least `SECRET_KEY`, database credentials if you change them, and `API_TELEGRAM_BOT_FATHER` if you use Telegram.

3. Start the stack:

   ```bash
   docker compose up --build
   ```

   API: **http://localhost:8000** (migrations run in the `app` service command).

4. Run tests inside Docker:

   ```bash
   docker compose run --rm test
   ```

> **Secrets:** do not commit real keys. Use `.env` (ignored by git) or your host/CI secret store. `docker-compose.yml` reads variables from the environment / `.env` file in the project root.

## Local run (without Docker)

You need **PostgreSQL** and **Redis** running locally (or tunneled). Match `NAME`, `USER`, `PASSWORD`, `HOST`, `PORT`, and Redis URLs in `.env` to your setup.

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate  # Linux/macOS

pip install -r requirements.txt
cp .env.sample .env   # then edit HOST=127.0.0.1 etc.

python manage.py migrate
python manage.py runserver
```

Optional — if you use **Poetry**, install from `pyproject.toml` / lockfile (note: Docker and CI use `requirements.txt` as the canonical dependency list for parity).

## Celery (local)

```bash
celery -A config worker -l info
celery -A config beat -l info
```

## CI

GitHub Actions runs on pushes/PRs to `main` / `develop`: **Python 3.13**, **PostgreSQL 15**, **Redis 7**, then `pip install -r requirements.txt` and `python manage.py test`.  
Workflow file: [`.github/workflows/tests.yml`](.github/workflows/tests.yml).

## Roadmap

- More integration tests and coverage.
- Docker Secrets / external secret manager for production keys.
- Gamification (levels, streaks, etc.).
