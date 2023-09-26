from django.contrib import admin
from django.urls import path

from managers import CustomUserManager


urlpatterns = [
    path("admin/", admin.site.urls),
    path("create_user/", CustomUserManager.create_user),
    path("create_superuser/", CustomUserManager.create_superuser),
]
