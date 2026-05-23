from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from .constants import (
    JSON_STATUS_OK,
    PROJECT_STATUS_CLOSED,
    PROJECT_STATUS_OPEN,
    URL_NAME_COMPLETE,
    URL_NAME_LIST,
    URL_NAME_SKILL_ADD,
    URL_NAME_SKILLS_AUTOCOMPLETE,
)
from .models import Project, Skill

User = get_user_model()

TEST_EMAIL = "test@example.com"
TEST_PASSWORD = "password123"
TEST_USER_NAME = "Тест"
TEST_USER_SURNAME = "Пользователь"
TEST_PROJECT_NAME = "Тестовый проект"
TEST_PROJECT_DESCRIPTION = "Описание"
TEST_SKILL_NAME = "Python"
TEST_SKILL_QUERY = "Py"
TEST_SKILL_NEW_NAME = "Django"
TEST_SKILL_FILTER_OTHER = "Rust"


class ProjectViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email=TEST_EMAIL,
            name=TEST_USER_NAME,
            surname=TEST_USER_SURNAME,
            password=TEST_PASSWORD,
        )
        self.skill = Skill.objects.create(name=TEST_SKILL_NAME)
        self.project = Project.objects.create(
            name=TEST_PROJECT_NAME,
            description=TEST_PROJECT_DESCRIPTION,
            owner=self.user,
            status=PROJECT_STATUS_OPEN,
        )
        self.project.participants.add(self.user)
        self.project.skills.add(self.skill)

    def test_project_list_page(self):
        response = self.client.get(reverse(URL_NAME_LIST))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, TEST_PROJECT_NAME)

    def test_project_filter_by_skill(self):
        response = self.client.get(reverse(URL_NAME_LIST), {"skill": TEST_SKILL_NAME})
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, TEST_PROJECT_NAME)

        response = self.client.get(
            reverse(URL_NAME_LIST),
            {"skill": TEST_SKILL_FILTER_OTHER},
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertNotContains(response, TEST_PROJECT_NAME)

    def test_skills_autocomplete(self):
        response = self.client.get(
            reverse(URL_NAME_SKILLS_AUTOCOMPLETE),
            {"q": TEST_SKILL_QUERY},
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], TEST_SKILL_NAME)

    def test_add_skill_requires_login(self):
        url = reverse(URL_NAME_SKILL_ADD, kwargs={"pk": self.project.pk})
        response = self.client.post(
            url,
            data=f'{{"name": "{TEST_SKILL_NEW_NAME}"}}',
            content_type="application/json",
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_add_skill_as_owner(self):
        self.client.login(username=TEST_EMAIL, password=TEST_PASSWORD)
        url = reverse(URL_NAME_SKILL_ADD, kwargs={"pk": self.project.pk})
        response = self.client.post(
            url,
            data=f'{{"name": "{TEST_SKILL_NEW_NAME}"}}',
            content_type="application/json",
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        data = response.json()
        self.assertTrue(data["added"])
        self.assertTrue(data["created"])
        self.assertIn("skill_id", data)
        self.assertNotIn("name", data)
        self.assertTrue(self.project.skills.filter(name=TEST_SKILL_NEW_NAME).exists())

    def test_complete_project(self):
        self.client.login(username=TEST_EMAIL, password=TEST_PASSWORD)
        url = reverse(URL_NAME_COMPLETE, kwargs={"pk": self.project.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        data = response.json()
        self.assertEqual(data["status"], JSON_STATUS_OK)
        self.assertEqual(data["project_status"], PROJECT_STATUS_CLOSED)
        self.project.refresh_from_db()
        self.assertEqual(self.project.status, PROJECT_STATUS_CLOSED)
