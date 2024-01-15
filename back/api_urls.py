from rest_framework.routers import DefaultRouter
from django.urls import include, path, re_path

router = DefaultRouter()

urlpatterns = [
    path("users/", include("back.apps.users.urls")),
    path("courses/", include("back.apps.courses.urls")),
    path("", include(router.urls)),
]
