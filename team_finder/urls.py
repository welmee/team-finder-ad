from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", lambda request: redirect("projects:list")),
    path("admin/", admin.site.urls),
    path("users/", include("apps.users.urls")),
    path("projects/", include("apps.projects.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
