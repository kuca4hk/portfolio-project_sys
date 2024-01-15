# serializers.py

from rest_framework import serializers
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    password = (
        serializers.CharField()
    )  # Zde definujeme pole pro heslo, write_only zajistí, že heslo nebude vráceno při serializaci

    class Meta:
        model = CustomUser
        fields = "__all__"  # Zahrnujeme jen potřebná pole


class RegistrationUserSerializer(serializers.ModelSerializer):
    password = (
        serializers.CharField()
    )  # Zde definujeme pole pro heslo, write_only zajistí, že heslo nebude vráceno při serializaci

    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "last_name",
            "email",
            "password",
            "adress",
            "city",
            "zip_code",
        ]  # Zahrnujeme jen potřebná pole

    def create(self, validated_data):
        password = validated_data.pop("password")  # Vyjmutí hesla z dat pro validaci
        user = CustomUser.objects.create(
            **validated_data
        )  # Vytvoření uživatele bez hesla
        user.set_password(password)  # Nastavení hesla
        user.save()  # Uložení uživatele s novým heslem
        return user
