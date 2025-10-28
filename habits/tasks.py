from datetime import datetime

import requests
from celery import shared_task

from config.settings import API_TELEGRAM_BOT_FATHER
from habits.models import Habit


@shared_task
def send_habit_message():
    """Переодическая задача, которая при наступлении даты, которую указал пользователь отправляет ему сообщение в телеграмм боте."""

    url = f"https://api.telegram.org/bot{API_TELEGRAM_BOT_FATHER}/sendMessage"

    habits = Habit.objects.all()
    for habit in habits:
        if habit.chat_id:
            habit_time = habit.time.strftime("%Y-%m-%d %H:%M")
            datetime_now = datetime.now().strftime("%Y-%m-%d %H:%M")
            if habit_time == datetime_now:
                params = {
                    "chat_id": habit.chat_id,
                    "text": f"Я буду '{habit.action}' в '{habit.time}' в '{habit.place}', за {habit.time_to_complete} секунд",
                }

                try:
                    response = requests.post(url, params=params)
                    response.raise_for_status()
                    print("True")
                except requests.exceptions.RequestException as e:
                    print(f"Ошибка отправки сообщения в Telegram: {e}")
