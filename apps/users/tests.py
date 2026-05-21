from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()


class UserViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="alice@example.com",
            name="Алиса",
            surname="Смирнова",
            password="password123",
        )

    def test_register_logs_in_and_redirects_to_projects(self):
        response = self.client.post(
            reverse("users:register"),
            {
                "name": "Борис",
                "surname": "Иванов",
                "email": "bob@example.com",
                "password": "password123",
            },
        )
        self.assertRedirects(response, reverse("projects:list"))
        self.assertTrue(User.objects.filter(email="bob@example.com").exists())
        user = User.objects.get(email="bob@example.com")
        self.assertTrue(user.avatar)
        self.assertEqual(user.phone, "")

    def test_login_success(self):
        response = self.client.post(
            reverse("users:login"),
            {"email": "alice@example.com", "password": "password123"},
        )
        self.assertRedirects(response, reverse("projects:list"))

    def test_participants_list(self):
        response = self.client.get(reverse("users:list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Алиса")

    def test_user_profile(self):
        response = self.client.get(reverse("users:detail", kwargs={"pk": self.user.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Смирнова")
