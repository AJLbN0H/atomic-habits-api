from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User

class UserTestCase(APITestCase):

    def setUp(self):
        self.user = User(email="test@test.com")
        self.user.set_password("testpassword")
        self.user.save()

    def test_user_registration(self):
        """Тест регистрации пользователя."""
        url = reverse("users:register")
        data = {
            "email": "newuser@test.com",
            "password": "newpassword123",
            "city": "Moscow"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.filter(email="newuser@test.com").count(), 1)
        # Проверяем, что пароль захеширован
        new_user = User.objects.get(email="newuser@test.com")
        self.assertTrue(new_user.check_password("newpassword123"))

    def test_user_login(self):
        """Тест авторизации пользователя и получения токена."""
        url = reverse("users:login")
        data = {
            "email": "test@test.com",
            "password": "testpassword"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
