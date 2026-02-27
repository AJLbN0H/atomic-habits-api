# Atomic Habits: Backend для трекера привычек

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![Django](https://img.shields.io/badge/django-5.2+-green.svg)
![Celery](https://img.shields.io/badge/celery--beat-enabled-orange.svg)
![Redis](https://img.shields.io/badge/redis-broker-red.svg)

**Atomic Habits API** — это бэкенд-сервис для создания и контроля полезных привычек. Проект вдохновлен книгой "Атомные привычки" и включает в себя сложную бизнес-логику валидации, планирования задач и интеграции с внешними сервисами.

## Ключевой функционал
* **Управление привычками:** CRUD операций с разделением на "привычки" и "вознаграждения".
* **Умная валидация:** Кастомные валидаторы на уровне сериализаторов (исключение конфликтов между вознаграждением и связанной привычкой).
* **Автоматические напоминания:** Использование Celery Beat для ежедневной проверки и отправки уведомлений пользователям.
* **Публичный доступ:** Механизм публикации привычек для обмена опытом внутри сообщества.
* **Настройка периодичности:** Поддержка гибких графиков выполнения (ежедневно, раз в неделю и т.д.).

## Технологический стек
* **Framework:** Django Rest Framework (DRF).
* **Task Scheduling:** Celery + Celery Beat.
* **Message Broker:** Redis.
* **Database:** PostgreSQL.
* **Auth:** JWT Authentication.

## Архитектура решения
Проект построен на принципах чистой архитектуры:
* habits/: Основная логика, модели и кастомные валидаторы.
* users/: Управление аккаунтами и доступами.
* services/: Логика интеграции (например, отправка сообщений в Telegram).

## Установка и запуск

1. Клонируйте репозиторий:

    git clone https://github.com/AJLbN0H/atomic-habits-api.git

2. Настройте файл .env:
Укажите параметры PostgreSQL, Redis и токен вашего Telegram-бота.

3. Запустите инфраструктуру через Docker:

    docker-compose up --build

4. Локальный запуск (требуется установленный Redis):

    poetry install
    python manage.py migrate
    python manage.py runserver

## Команды для запуска фоновых процессов:
* Запуск воркера Celery: `celery -A config worker -l info`
* Запуск планировщика Beat: `celery -A config beat -l info`

## Roadmap
* Покрытие кода интеграционными тестами.
* Интеграция с Docker Secrets для безопасного хранения API-ключей.
* Добавление системы "уровней" и геймификации для пользователей.
