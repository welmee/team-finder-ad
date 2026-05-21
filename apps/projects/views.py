import json

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

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

    paginator = Paginator(projects, 12)
    page_obj = paginator.get_page(request.GET.get("page"))

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


@login_required
@require_POST
def complete_project_view(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    if project.status != "open":
        return JsonResponse(
            {"status": "error", "message": "Проект уже завершён"},
            status=400,
        )
    project.status = "closed"
    project.save(update_fields=["status"])
    return JsonResponse({"status": "ok", "project_status": "closed"})


@login_required
@require_POST
def toggle_participate_view(request, pk):
    project = get_object_or_404(Project, pk=pk)
    user = request.user
    if project.participants.filter(pk=user.pk).exists():
        project.participants.remove(user)
        participating = False
    else:
        project.participants.add(user)
        participating = True
    return JsonResponse({"status": "ok", "participant": participating})


def skills_autocomplete_view(request):
    q = request.GET.get("q", "").strip()
    skills = Skill.objects.filter(name__istartswith=q).order_by("name")[:10]
    return JsonResponse(list(skills.values("id", "name")), safe=False)


@login_required
@require_POST
def add_skill_view(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    try:
        body = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    skill_id = body.get("skill_id")
    name = body.get("name", "").strip()
    created = False
    added = False

    if skill_id:
        skill = get_object_or_404(Skill, pk=skill_id)
    elif name:
        skill, created = Skill.objects.get_or_create(name=name)
    else:
        return JsonResponse({"error": "skill_id or name required"}, status=400)

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
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    skill = get_object_or_404(Skill, pk=skill_id)
    if not project.skills.filter(pk=skill.pk).exists():
        return JsonResponse(
            {"status": "error", "message": "Навык не привязан к проекту"},
            status=400,
        )
    project.skills.remove(skill)
    return JsonResponse({"status": "ok"})
