from rest_framework.routers import DefaultRouter
from django.urls import include, path, re_path
from .views import (
    get_user_information,
    UserLoginView,
    registration_user,
    change_password,
    logout_view,
)


router = DefaultRouter()
# router.register(r'user-infromation', get_user_information, basename='user-infromation')

urlpatterns = [
    # LOGIN
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
    path("change-password/", change_password, name="logout"),
    path("user-information/<int:id>/", get_user_information, name="user-information"),
    path("registration/", registration_user, name="reqistration-user"),
    path("", include(router.urls)),
]

urlpatterns += router.urls
