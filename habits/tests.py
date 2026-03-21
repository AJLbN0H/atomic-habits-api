from datetime import timedelta
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User


class HabitTestCase(APITestCase):

    def setUp(self):
        self.user = User(email="habituser@test.com")
        self.user.set_password("habitpass")
        self.user.save()
        
        self.client.force_authenticate(user=self.user)
        
        # Приятная привычка для тестов связывания
        self.pleasant_habit = Habit.objects.create(
            user=self.user,
            place="Дома",
            time=timezone.now(),
            action="Съесть яблоко",
            a_sign_of_a_pleasant_habit=True,
            time_to_complete=60,
            periodicity=1
        )
        
        self.habit = Habit.objects.create(
            user=self.user,
            place="Парк",
            time=timezone.now(),
            action="Пробежать 5 км",
            time_to_complete=100,
            periodicity=1,
            reward="Мороженое"
        )

    def test_habit_create(self):
        """Тестирование создания привычки"""
        url = reverse("habits:habits_create")
        data = {
            "place": "Зал",
            "time": (timezone.now() + timedelta(days=1)).isoformat(),
            "action": "Тренировка",
            "time_to_complete": 90,
            "periodicity": 2,
            "reward": "Протеиновый коктейль"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 3)
        self.assertEqual(Habit.objects.get(id=response.data["id"]).user, self.user)

    def test_habit_validation_time_to_complete(self):
        """Тест валидации времени выполнения (> 120 секунд)"""
        url = reverse("habits:habits_create")
        data = {
            "place": "Зал",
            "time": timezone.now().isoformat(),
            "action": "Тренировка",
            "time_to_complete": 130, # Слишком долго
            "periodicity": 1,
            "reward": "Коктейль"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)

    def test_habit_validation_reward_and_associated(self):
        """Тест валидации одновременного выбора вознаграждения и приятной привычки"""
        url = reverse("habits:habits_create")
        data = {
            "place": "Зал",
            "time": timezone.now().isoformat(),
            "action": "Тренировка",
            "time_to_complete": 90,
            "periodicity": 1,
            "reward": "Коктейль",
            "associated_habit": self.pleasant_habit.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)

    def test_habit_list(self):
        """Тестирование вывода списка привычек пользователя"""
        url = reverse("habits:habits_user_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # 1 обычная + 1 приятная из setUp
        self.assertEqual(response.data["count"], 2)

    def test_habit_update(self):
        """Тестирование обновления привычки"""
        url = reverse("habits:habits_update", args=(self.habit.id,))
        data = {
            "action": "Пробежать 10 км"
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Habit.objects.get(id=self.habit.id).action, "Пробежать 10 км")

    def test_habit_delete(self):
        """Тестирование удаления привычки"""
        url = reverse("habits:habits_delete", args=(self.habit.id,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 1)

    def test_habit_validation_periodicity(self):
        """Тест валидации периодичности (> 7 дней)"""
        url = reverse("habits:habits_create")
        data = {
            "place": "Дом",
            "time": timezone.now().isoformat(),
            "action": "Чтение",
            "time_to_complete": 60,
            "periodicity": 8, # Слишком редко
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)

    def test_habit_validation_chat_id(self):
        """Тест валидации chat_id (должен быть 10 цифр)"""
        url = reverse("habits:habits_create")
        data = {
            "place": "Дом",
            "time": timezone.now().isoformat(),
            "action": "Чтение",
            "time_to_complete": 60,
            "periodicity": 1,
            "chat_id": "123" # Слишком короткий
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)

    def test_habit_permission_is_owner(self):
        """Тест прав доступа: пользователь не может редактировать чужую привычку"""
        # Создаем другого пользователя
        another_user = User.objects.create(email="other@test.com")
        another_user.set_password("otherpass")
        another_user.save()
        
        # Переключаемся на другого пользователя
        self.client.force_authenticate(user=another_user)
        
        url = reverse("habits:habits_update", args=(self.habit.id,))
        data = {"action": "Взломанное действие"}
        response = self.client.patch(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_public_habits_list(self):
        """Тестирование списка публичных привычек"""
        # Делаем привычку публичной
        self.habit.publication_sign = True
        self.habit.save()
        
        url = reverse("habits:habits_public_list")
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # В списке должна быть как минимум 1 привычка
        self.assertTrue(len(response.data["results"]) >= 1)
        self.assertEqual(response.data["results"][0]["id"], self.habit.id)
