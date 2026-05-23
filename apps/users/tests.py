from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from .constants import (
    URL_NAME_DETAIL,
    URL_NAME_LIST,
    URL_NAME_LOGIN,
    URL_NAME_PROJECTS_LIST,
    URL_NAME_REGISTER,
)

User = get_user_model()

TEST_EMAIL = "alice@example.com"
TEST_PASSWORD = "password123"
TEST_USER_NAME = "Алиса"
TEST_USER_SURNAME = "Смирнова"
TEST_REGISTER_NAME = "Борис"
TEST_REGISTER_SURNAME = "Иванов"
TEST_REGISTER_EMAIL = "bob@example.com"


class UserViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email=TEST_EMAIL,
            name=TEST_USER_NAME,
            surname=TEST_USER_SURNAME,
            password=TEST_PASSWORD,
        )

    def test_register_logs_in_and_redirects_to_projects(self):
        response = self.client.post(
            reverse(URL_NAME_REGISTER),
            {
                "name": TEST_REGISTER_NAME,
                "surname": TEST_REGISTER_SURNAME,
                "email": TEST_REGISTER_EMAIL,
                "password": TEST_PASSWORD,
            },
        )
        self.assertRedirects(response, reverse(URL_NAME_PROJECTS_LIST))
        self.assertTrue(User.objects.filter(email=TEST_REGISTER_EMAIL).exists())
        user = User.objects.get(email=TEST_REGISTER_EMAIL)
        self.assertTrue(user.avatar)
        self.assertEqual(user.phone, "")

    def test_login_success(self):
        response = self.client.post(
            reverse(URL_NAME_LOGIN),
            {"email": TEST_EMAIL, "password": TEST_PASSWORD},
        )
        self.assertRedirects(response, reverse(URL_NAME_PROJECTS_LIST))

    def test_participants_list(self):
        response = self.client.get(reverse(URL_NAME_LIST))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, TEST_USER_NAME)

    def test_user_profile(self):
        response = self.client.get(reverse(URL_NAME_DETAIL, kwargs={"pk": self.user.pk}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, TEST_USER_SURNAME)
