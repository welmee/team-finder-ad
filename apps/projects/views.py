import json
from http import HTTPStatus

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from team_finder.pagination import paginate_queryset

from .constants import (
    JSON_STATUS_ERROR,
    JSON_STATUS_OK,
    MSG_INVALID_JSON,
    MSG_NOT_FOUND,
    MSG_PROJECT_ALREADY_COMPLETED,
    MSG_SKILL_ID_OR_NAME_REQUIRED,
    MSG_SKILL_NOT_LINKED,
    PROJECT_STATUS_CLOSED,
    PROJECT_STATUS_OPEN,
    SKILLS_AUTOCOMPLETE_LIMIT,
)
from .forms import ProjectForm
from .models import Project, Skill


def project_list_view(request):
    projects = Project.objects.select_related("owner").prefetch_related(
        "participants", "skills"
    ).order_by("-created_at")

    all_skills = Skill.objects.all()
    active_skill = request.GET.get("skill", "").strip()

    if active_skill:
        projects = projects.filter(skills__name=active_skill).distinct()

    page_obj = paginate_queryset(request, projects)

    return render(request, "projects/project_list.html", {
        "projects": page_obj,
        "all_skills": all_skills,
        "active_skill": active_skill,
    })


def project_detail_view(request, pk):
    project = get_object_or_404(
        Project.objects.select_related("owner").prefetch_related("participants", "skills"),
        pk=pk,
    )
    return render(request, "projects/project-details.html", {"project": project})


@login_required
def create_project_view(request):
    form = ProjectForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        project = form.save(commit=False)
        project.owner = request.user
        project.save()
        project.participants.add(request.user)
        return redirect("projects:detail", pk=project.pk)
    return render(request, "projects/create-project.html", {"form": form, "is_edit": False})


@login_required
def edit_project_view(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    form = ProjectForm(request.POST or None, instance=project)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("projects:detail", pk=project.pk)
    return render(request, "projects/create-project.html", {"form": form, "is_edit": True})


def _json_not_found(message=MSG_NOT_FOUND):
    return JsonResponse({"error": message}, status=HTTPStatus.NOT_FOUND)


@login_required
@require_POST
def complete_project_view(request, pk):
    project = Project.objects.filter(pk=pk, owner=request.user).first()
    if project is None:
        return _json_not_found()
    if project.status != PROJECT_STATUS_OPEN:
        return JsonResponse(
            {"status": JSON_STATUS_ERROR, "message": MSG_PROJECT_ALREADY_COMPLETED},
            status=HTTPStatus.BAD_REQUEST,
        )
    project.status = PROJECT_STATUS_CLOSED
    project.save(update_fields=["status"])
    return JsonResponse({"status": JSON_STATUS_OK, "project_status": PROJECT_STATUS_CLOSED})


@login_required
@require_POST
def toggle_participate_view(request, pk):
    project = Project.objects.filter(pk=pk).first()
    if project is None:
        return _json_not_found()
    user = request.user
    was_participating = project.participants.filter(pk=user.pk).exists()
    if was_participating:
        project.participants.remove(user)
    else:
        project.participants.add(user)
    return JsonResponse({"status": JSON_STATUS_OK, "participant": not was_participating})


def skills_autocomplete_view(request):
    query = request.GET.get("q", "").strip()
    skills = Skill.objects.filter(name__istartswith=query).order_by("name")[
        :SKILLS_AUTOCOMPLETE_LIMIT
    ]
    return JsonResponse(list(skills.values("id", "name")), safe=False)


@login_required
@require_POST
def add_skill_view(request, pk):
    project = Project.objects.filter(pk=pk, owner=request.user).first()
    if project is None:
        return _json_not_found()
    try:
        body = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({"error": MSG_INVALID_JSON}, status=HTTPStatus.BAD_REQUEST)

    skill_id = body.get("skill_id")
    name = body.get("name", "").strip()
    created = False
    added = False

    if skill_id:
        skill = Skill.objects.filter(pk=skill_id).first()
        if skill is None:
            return _json_not_found()
    elif name:
        skill, created = Skill.objects.get_or_create(name=name)
    else:
        return JsonResponse(
            {"error": MSG_SKILL_ID_OR_NAME_REQUIRED},
            status=HTTPStatus.BAD_REQUEST,
        )

    if not project.skills.filter(pk=skill.pk).exists():
        project.skills.add(skill)
        added = True

    return JsonResponse({
        "skill_id": skill.pk,
        "created": created,
        "added": added,
    })


@login_required
@require_POST
def remove_skill_view(request, pk, skill_id):
    project = Project.objects.filter(pk=pk, owner=request.user).first()
    if project is None:
        return _json_not_found()
    skill = Skill.objects.filter(pk=skill_id).first()
    if skill is None:
        return _json_not_found()
    if not project.skills.filter(pk=skill.pk).exists():
        return JsonResponse(
            {"status": JSON_STATUS_ERROR, "message": MSG_SKILL_NOT_LINKED},
            status=HTTPStatus.BAD_REQUEST,
        )
    project.skills.remove(skill)
    return JsonResponse({"status": JSON_STATUS_OK})
