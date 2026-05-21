# Team Finder — Вариант 3 (Навыки проектов и фильтрация)

## Инструкция для ревьюера

### Быстрый старт через Docker Compose (рекомендуется)

Это самый простой способ запустить весь проект одной командой.

**Требования:** Docker и Docker Compose.

```bash
# 1. Клонировать репозиторий
git clone <url> && cd team-finder-ad-main-3

# 2. Создать .env (заполнен по умолчанию)
cp .env_example .env

# 3. Запустить всё (БД + Django + миграции + тестовые данные)
docker compose up --build
```

Проект будет доступен по адресу: **http://localhost:8000**

Тестовые данные (пользователи и проекты) загружаются автоматически.

---

### Локальный запуск (без Docker)

**Требования:** Python 3.12+, PostgreSQL 16.

```bash
# 1. Создать виртуальное окружение
python3 -m venv venv
source venv/bin/activate          # Linux/Mac
# venv\Scripts\activate           # Windows

# 2. Установить зависимости
pip install -r requirements.txt

# 3. Создать .env файл
cp .env_example .env
# Отредактировать .env: укажите параметры PostgreSQL и TASK_VERSION=3

# 4. Запустить PostgreSQL (если нет локального, используйте Docker):
docker compose up -d db

# 5. Применить миграции
python manage.py migrate

# 6. Загрузить тестовые данные
python manage.py seed_data

# 7. Запустить сервер
python manage.py runserver
```

Проект доступен по адресу: **http://localhost:8000**

---

### Тестовые пользователи

| Email | Пароль | Имя |
|---|---|---|
| `alice@example.com` | `password123` | Алиса Смирнова |
| `bob@example.com` | `password123` | Борис Иванов |
| `carol@example.com` | `password123` | Карина Петрова |
| `david@example.com` | `password123` | Дмитрий Козлов |
| `eva@example.com` | `password123` | Ева Новикова |
| `admin@example.com` | `admin123` | Admin (суперпользователь) |

У каждого пользователя создано по 2 проекта с навыками.

Панель администратора: **http://localhost:8000/admin/**

---

### Структура проекта

```
team-finder-ad-main-3/
├── apps/
│   ├── users/          # Кастомная модель User, регистрация, авторизация
│   └── projects/       # Модели Project и Skill, все CRUD операции
├── team_finder/        # Настройки Django
├── templates_var3/     # HTML-шаблоны для варианта 3
├── static/             # CSS, JS, изображения
├── media/              # Загружаемые файлы (аватары)
├── docker-compose.yml  # БД PostgreSQL + Django
├── Dockerfile
├── requirements.txt
└── .env_example
```

---

### Особенности варианта 3

- **Навыки проектов:** на странице проекта отображается блок "Необходимые навыки"
- **Управление навыками без перезагрузки:** добавление/удаление навыков через AJAX
- **Автодополнение навыков:** при вводе предлагаются существующие навыки (GET `/projects/skills/?q=...`)
- **Создание нового навыка:** если навык не найден, можно создать прямо из поля ввода
- **Фильтрация проектов:** на главной странице можно фильтровать проекты по навыку (`?skill=Python`)
- **Активный фильтр подсвечивается** и есть кнопка сброса

---

### Переменные окружения (.env)

| Переменная | Значение по умолчанию | Описание |
|---|---|---|
| `DJANGO_SECRET_KEY` | — | Секретный ключ Django |
| `DJANGO_DEBUG` | `True` | Режим отладки |
| `POSTGRES_DB` | `team_finder` | Имя БД |
| `POSTGRES_USER` | `team_finder` | Пользователь БД |
| `POSTGRES_PASSWORD` | `team_finder` | Пароль БД |
| `POSTGRES_HOST` | `localhost` | Хост БД (`db` в Docker) |
| `POSTGRES_PORT` | `5432` | Порт БД |
| `TASK_VERSION` | `3` | Вариант шаблонов (обязательно `3`) |
