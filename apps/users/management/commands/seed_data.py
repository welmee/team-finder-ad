"""Management command to seed the database with test users and projects."""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.projects.models import Project, Skill

User = get_user_model()

SKILLS = [
    "Python", "Django", "JavaScript", "React", "Vue.js",
    "PostgreSQL", "Docker", "Git", "Machine Learning", "Data Science",
    "Golang", "Rust", "Flutter", "iOS", "Android",
]

USERS = [
    {
        "email": "alice@example.com",
        "name": "Алиса",
        "surname": "Смирнова",
        "phone": "89001111111",
        "about": "Backend-разработчик, люблю Python и Django.",
        "github_url": "https://github.com/alice",
        "password": "password123",
    },
    {
        "email": "bob@example.com",
        "name": "Борис",
        "surname": "Иванов",
        "phone": "89002222222",
        "about": "Fullstack-разработчик. React + Node.js.",
        "github_url": "https://github.com/bob",
        "password": "password123",
    },
    {
        "email": "carol@example.com",
        "name": "Карина",
        "surname": "Петрова",
        "phone": "89003333333",
        "about": "Data Scientist, ML-энтузиаст.",
        "github_url": "https://github.com/carol",
        "password": "password123",
    },
    {
        "email": "david@example.com",
        "name": "Дмитрий",
        "surname": "Козлов",
        "phone": "89004444444",
        "about": "DevOps инженер. Docker, Kubernetes, CI/CD.",
        "github_url": "https://github.com/david",
        "password": "password123",
    },
    {
        "email": "eva@example.com",
        "name": "Ева",
        "surname": "Новикова",
        "phone": "89005555555",
        "about": "Мобильная разработка (Flutter/iOS).",
        "github_url": "https://github.com/eva",
        "password": "password123",
    },
]

PROJECTS = [
    {
        "owner_email": "alice@example.com",
        "name": "TeamSync — система управления командами",
        "description": (
            "Веб-приложение для управления распределёнными командами разработчиков. "
            "Включает доску задач, трекер времени и интеграцию с GitHub."
        ),
        "status": "open",
        "github_url": "https://github.com/alice/teamsync",
        "skills": ["Python", "Django", "PostgreSQL", "React"],
    },
    {
        "owner_email": "alice@example.com",
        "name": "SmartBudget — персональные финансы",
        "description": (
            "Приложение для учёта личных финансов с категоризацией расходов, "
            "прогнозами на основе ML и красивыми графиками."
        ),
        "status": "open",
        "github_url": "https://github.com/alice/smartbudget",
        "skills": ["Python", "Django", "Machine Learning", "PostgreSQL"],
    },
    {
        "owner_email": "bob@example.com",
        "name": "CodeReview Bot — автоматический ревьювер",
        "description": (
            "Telegram-бот, который анализирует pull-request'ы и даёт советы "
            "по улучшению кода. Использует OpenAI API."
        ),
        "status": "open",
        "github_url": "https://github.com/bob/codereview-bot",
        "skills": ["Python", "JavaScript", "Git"],
    },
    {
        "owner_email": "bob@example.com",
        "name": "OpenMap — карта открытых событий",
        "description": (
            "Интерактивная карта городских событий: концерты, митапы, мастер-классы. "
            "Пользователи могут добавлять и находить мероприятия рядом."
        ),
        "status": "closed",
        "github_url": "https://github.com/bob/openmap",
        "skills": ["React", "Django", "PostgreSQL", "Docker"],
    },
    {
        "owner_email": "carol@example.com",
        "name": "NLP Corpus — обработка русских текстов",
        "description": (
            "Инструментарий для работы с русскоязычными корпусами: токенизация, "
            "лемматизация, анализ тональности и тематическое моделирование."
        ),
        "status": "open",
        "github_url": "https://github.com/carol/nlp-corpus",
        "skills": ["Python", "Machine Learning", "Data Science"],
    },
    {
        "owner_email": "carol@example.com",
        "name": "RecSys — система рекомендаций контента",
        "description": (
            "Рекомендательная система для стриминговой платформы. "
            "Коллаборативная и контентная фильтрация, A/B тесты."
        ),
        "status": "open",
        "github_url": "https://github.com/carol/recsys",
        "skills": ["Python", "Machine Learning", "Data Science", "PostgreSQL"],
    },
    {
        "owner_email": "david@example.com",
        "name": "K8s Dashboard Lite — упрощённая панель Kubernetes",
        "description": (
            "Лёгкая альтернатива официального дашборда Kubernetes. "
            "Мониторинг подов, логи, метрики в одном интерфейсе."
        ),
        "status": "open",
        "github_url": "https://github.com/david/k8s-dashboard-lite",
        "skills": ["Golang", "Docker", "React"],
    },
    {
        "owner_email": "david@example.com",
        "name": "CI/CD Templates — библиотека пайплайнов",
        "description": (
            "Коллекция готовых шаблонов GitHub Actions и GitLab CI для типичных "
            "стеков: Django, Node.js, Go, Flutter."
        ),
        "status": "open",
        "github_url": "https://github.com/david/cicd-templates",
        "skills": ["Docker", "Git", "Golang"],
    },
    {
        "owner_email": "eva@example.com",
        "name": "MindfulMe — приложение для медитаций",
        "description": (
            "Кроссплатформенное мобильное приложение с таймером медитаций, "
            "дневником настроения и персональными напоминаниями."
        ),
        "status": "open",
        "github_url": "https://github.com/eva/mindfulme",
        "skills": ["Flutter", "iOS", "Android"],
    },
    {
        "owner_email": "eva@example.com",
        "name": "TravelBuddy — планировщик путешествий",
        "description": (
            "Мобильный помощник путешественника: маршруты, бюджет, офлайн-карты, "
            "заметки и фотоотчёты по каждой поездке."
        ),
        "status": "closed",
        "github_url": "https://github.com/eva/travelbuddy",
        "skills": ["Flutter", "iOS", "Android", "Python"],
    },
]


class Command(BaseCommand):
    help = "Seed database with test users and projects"

    def handle(self, *args, **options):
        self.stdout.write("Creating skills...")
        skill_map = {}
        for name in SKILLS:
            skill, _ = Skill.objects.get_or_create(name=name)
            skill_map[name] = skill

        self.stdout.write("Creating users...")
        user_map = {}
        for data in USERS:
            if User.objects.filter(email=data["email"]).exists():
                user = User.objects.get(email=data["email"])
                self.stdout.write(f"  User {data['email']} already exists, skipping.")
            else:
                user = User.objects.create_user(
                    email=data["email"],
                    name=data["name"],
                    surname=data["surname"],
                    password=data["password"],
                    phone=data.get("phone", ""),
                    about=data.get("about", ""),
                    github_url=data.get("github_url", ""),
                )
                self.stdout.write(f"  Created user: {data['email']}")
            user_map[data["email"]] = user

        # Create admin if not exists
        if not User.objects.filter(email="admin@example.com").exists():
            User.objects.create_superuser(
                email="admin@example.com",
                name="Admin",
                surname="User",
                password="admin123",
            )
            self.stdout.write("  Created superuser: admin@example.com")

        self.stdout.write("Creating projects...")
        for data in PROJECTS:
            owner = user_map[data["owner_email"]]
            if Project.objects.filter(name=data["name"], owner=owner).exists():
                self.stdout.write(f"  Project '{data['name']}' already exists, skipping.")
                continue
            project = Project.objects.create(
                name=data["name"],
                description=data["description"],
                owner=owner,
                status=data["status"],
                github_url=data.get("github_url", ""),
            )
            project.participants.add(owner)
            for skill_name in data.get("skills", []):
                project.skills.add(skill_map[skill_name])
            self.stdout.write(f"  Created project: {data['name']}")

        self.stdout.write(self.style.SUCCESS("Done! Database seeded successfully."))
