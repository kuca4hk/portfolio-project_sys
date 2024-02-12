from rest_framework.routers import DefaultRouter
from django.urls import include, path, re_path
from .views import (
    get_courses,
    get_categories,
    get_course_detail,
    get_courses_by_category,
    create_course,
    update_course,
    users_course_registry,
    get_course_created_by_user,
    get_users_courses
)


router = DefaultRouter()
# router.register(r'user-infromation', get_user_information, basename='user-infromation')

urlpatterns = [
    # LOGIN
    path("courses/", get_courses, name="courses"),
    path("categories/", get_categories, name="categories"),
    path("course-detail/<int:id>/", get_course_detail, name="course-detail"),
    path("courses-by-category/<int:id>/", get_courses_by_category, name="courses-by-category"),
    path("create-course/", create_course, name="create-course"),
    path("update-course/<int:id>/", update_course, name="update-course"),
    path("users-course-registry/<int:id>/", users_course_registry, name="users-course-registry"),
    path("<int:id>/courses-created-by-user/", get_course_created_by_user, name="courses-created-by-user"),
    path("users-course-registry/", users_course_registry, name="users-course-registry"),
    path("my-courses-registration/",get_users_courses , name="my-courses")
]

urlpatterns += router.urls
