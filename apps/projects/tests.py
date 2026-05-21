from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from .models import Project, Skill

User = get_user_model()


class ProjectViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="test@example.com",
            name="Тест",
            surname="Пользователь",
            password="password123",
        )
        self.skill = Skill.objects.create(name="Python")
        self.project = Project.objects.create(
            name="Тестовый проект",
            description="Описание",
            owner=self.user,
            status="open",
        )
        self.project.participants.add(self.user)
        self.project.skills.add(self.skill)

    def test_project_list_page(self):
        response = self.client.get(reverse("projects:list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Тестовый проект")

    def test_project_filter_by_skill(self):
        response = self.client.get(reverse("projects:list"), {"skill": "Python"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Тестовый проект")

        response = self.client.get(reverse("projects:list"), {"skill": "Rust"})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Тестовый проект")

    def test_skills_autocomplete(self):
        response = self.client.get(reverse("projects:skills_autocomplete"), {"q": "Py"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], "Python")

    def test_add_skill_requires_login(self):
        url = reverse("projects:skill_add", kwargs={"pk": self.project.pk})
        response = self.client.post(
            url,
            data='{"name": "Django"}',
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 302)

    def test_add_skill_as_owner(self):
        self.client.login(username="test@example.com", password="password123")
        url = reverse("projects:skill_add", kwargs={"pk": self.project.pk})
        response = self.client.post(
            url,
            data='{"name": "Django"}',
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["added"])
        self.assertTrue(data["created"])
        self.assertIn("skill_id", data)
        self.assertNotIn("name", data)
        self.assertTrue(self.project.skills.filter(name="Django").exists())

    def test_complete_project(self):
        self.client.login(username="test@example.com", password="password123")
        url = reverse("projects:complete", kwargs={"pk": self.project.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "ok")
        self.assertEqual(data["project_status"], "closed")
        self.project.refresh_from_db()
        self.assertEqual(self.project.status, "closed")
