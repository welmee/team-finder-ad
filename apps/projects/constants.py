SKILL_NAME_MAX_LENGTH = 124
PROJECT_STATUS_MAX_LENGTH = 6

PROJECT_STATUS_OPEN = "open"
PROJECT_STATUS_CLOSED = "closed"

PROJECT_STATUS_CHOICES = [
    (PROJECT_STATUS_OPEN, "Open"),
    (PROJECT_STATUS_CLOSED, "Closed"),
]

SKILLS_AUTOCOMPLETE_LIMIT = 10

URL_NAME_LIST = "projects:list"
URL_NAME_DETAIL = "projects:detail"
URL_NAME_SKILLS_AUTOCOMPLETE = "projects:skills_autocomplete"
URL_NAME_SKILL_ADD = "projects:skill_add"
URL_NAME_COMPLETE = "projects:complete"

MSG_PROJECT_ALREADY_COMPLETED = "Проект уже завершён"
MSG_SKILL_NOT_LINKED = "Навык не привязан к проекту"
MSG_INVALID_JSON = "Invalid JSON"
MSG_SKILL_ID_OR_NAME_REQUIRED = "skill_id or name required"
MSG_NOT_FOUND = "Not found"

JSON_STATUS_OK = "ok"
JSON_STATUS_ERROR = "error"
