from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.viewsets import GenericViewSet

from .serializers import UserSerializer, RegistrationUserSerializer
from .models import CustomUser

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import authenticate, logout


class UserLoginView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print(request)
        email = request.user.email
        password = request.user.password

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND
            )

        if user.password == password and (
            user.role == "admin" or user.role == "instructor" or user.role == "user"
        ):
            serializer = UserSerializer(user)
            return Response(
                {"message": "Authenticated successfully", "user": serializer.data}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )


@api_view(["GET"])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_user_information(request, id):
    user = request.user
    if user:
        name = CustomUser.objects.get(pk=id)
        serializer = UserSerializer(name)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(
            {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def registration_user(request):
    serializer = RegistrationUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@authentication_classes([BasicAuthentication])  # Basic Authentication
@permission_classes([IsAuthenticated])  # Pouze pro autentizované uživatele
def logout_view(request):
    user = request.user
    logout(request)  # Odhlášení uživatele
    return Response(f"Uživatel {user} byl úspěšně odhlášen.")


@api_view(["POST"])
@authentication_classes([BasicAuthentication])  # Basic Authentication
@permission_classes([IsAuthenticated])  # Pouze pro autentizované uživatele
def change_password(request):
    # Získání aktuálního uživatele
    user = request.user
    user = CustomUser.objects.get(pk=user.id)
    if user:
        # Získání nového hesla z POST requestu

        new_password = request.data.get("new_password")
        if user.check_password(new_password):
            return Response(
                "New password can't be the same as old password.",
                status=status.HTTP_400_BAD_REQUEST,
            )
        confirm_new_password = request.data.get("confirm_new_password")

        if (
            confirm_new_password != new_password
        ):  # Předpokládá se, že heslo je v POST datu pod 'new_password'
            return Response(
                "Passwords does not match.", status=status.HTTP_400_BAD_REQUEST
            )
        # Změna hesla
        user.set_password(new_password)
        user.save()

        return Response("Password changed successfully.", status=status.HTTP_200_OK)
    else:
        return Response(
            {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )
