from django.shortcuts import render
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)

# Create your views here.
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Course, Category
from .serializers import (
    CourseSerializer,
    CategorySerializer,
    CourseDetailSerializer,
    CourseUpdateSerializer,
    CourseCreateSerializer,
    CourseUserSerializer,
)

from ..users.models import CustomUser


@api_view(["GET"])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_courses(request):
    courses = Course.objects.all()
    courses_active = courses.filter(is_active=True)
    serializer = CourseSerializer(courses_active, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(
        categories, many=True
    )  # TODO many=True je nutné, pokud vracíme seznam objektů
    return Response(serializer.data)


@api_view(["GET"])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_course_detail(request, id):
    course = Course.objects.get(pk=id)
    if course:
        serializer = CourseDetailSerializer(course)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(
            {"error": "Course does not exist"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_courses_by_category(request, id):
    courses = Course.objects.filter(category=id)
    if courses:
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(
            {"error": "Courses do not exist"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["POST", 'PUT'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def create_course(request):
    if request.method == "POST":
        serializer = CourseCreateSerializer(data=request.data)
        id_category = []
        for category in request.data['category']:
            cat = Category.objects.get(name=category)
            id_category.append(cat.id)
        request.data['category'] = id_category
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Course created"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "PUT":
        course = Course.objects.get(pk=request.data['id'])
        serializer = CourseCreateSerializer(course, data=request.data)
        id_category = []
        for category in request.data['category']:
            cat = Category.objects.get(name=category)
            id_category.append(cat.id)
        request.data['category'] = id_category
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Course created"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST", "PUT"])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def users_course_registry(request, id):
    course = Course.objects.get(pk=id)
    if course:
        if request.method == "POST":
            course.users.add(request.user)
            return Response(
                {"message": "User registered to course"}, status=status.HTTP_200_OK
            )
        elif request.method == "PUT":
            course.users.remove(request.user)
            return Response(
                {"message": "User unregistered from course"}, status=status.HTTP_200_OK
            )
    else:
        return Response(
            {"error": "Course does not exist"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_users_courses(request):
    user = request.user
    user = CustomUser.objects.get(email=user.email)
    courses = Course.objects.filter(users=user)
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["PUT"])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def update_course(request, id):
    user = request.user
    user = CustomUser.objects.get(email=user.email)
    course_user = Course.objects.get(created_by=user.email)
    if (
        user.role == "instructor"
        or user.role == "admin"
        and course_user.created_by == user
    ):
        course = Course.objects.get(pk=id)
        if course:
            serializer = CourseUpdateSerializer(course, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "Course updated"}, status=status.HTTP_200_OK
                )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"error": "Course does not exist"}, status=status.HTTP_404_NOT_FOUND
            )


@api_view(["GET"])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_course_created_by_user(request, id):
    user = request.user
    user = CustomUser.objects.get(id=id)
    courses = Course.objects.filter(created_by=user.id)
    if courses:
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(
            {"error": "Courses do not exist"}, status=status.HTTP_404_NOT_FOUND
        )