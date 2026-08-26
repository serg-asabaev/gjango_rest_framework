from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("weblearn.urls", namespace="weblearn")),
    path("users/", include("users.urls", namespace="users")),
]
