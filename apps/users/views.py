from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ChangePasswordForm, EditProfileForm, LoginForm, RegisterForm

User = get_user_model()


def register_view(request):
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = User.objects.create_user(
            email=form.cleaned_data["email"],
            name=form.cleaned_data["name"],
            surname=form.cleaned_data["surname"],
            password=form.cleaned_data["password"],
        )
        login(request, user)
        return redirect("projects:list")
    return render(request, "users/register.html", {"form": form})


def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data["email"],
            password=form.cleaned_data["password"],
        )
        if user is not None:
            login(request, user)
            return redirect("projects:list")
        form.add_error(None, "Неверный email или пароль")
    return render(request, "users/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("projects:list")


def user_detail_view(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, "users/user-details.html", {"user": user})


def participants_view(request):
    queryset = User.objects.all().order_by("-id")
    paginator = Paginator(queryset, 12)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "users/participants.html", {"participants": page_obj})


@login_required
def edit_profile_view(request):
    form = EditProfileForm(
        request.POST or None,
        request.FILES or None,
        instance=request.user,
    )
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("users:detail", pk=request.user.pk)
    return render(request, "users/edit_profile.html", {"form": form})


@login_required
def change_password_view(request):
    form = ChangePasswordForm(request.user, request.POST or None)
    if request.method == "POST" and form.is_valid():
        request.user.set_password(form.cleaned_data["new_password1"])
        request.user.save()
        login(request, request.user)
        return redirect("users:detail", pk=request.user.pk)
    return render(request, "users/change_password.html", {"form": form})
