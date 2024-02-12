# Create your tests here.
from django.test import TestCase
from .models import CustomUser
# Create your tests here.


class CustomUserTestCase(TestCase):
    def setUp(self):
        CustomUser.objects.create(
            email=" ",
            password=" ",
            first_name=" ",
            last_name=" ",
            adress=" ",
            city=" ")

    def test_custom_user(self):
        user = CustomUser.objects.get(email=" ")
        self.assertEqual(user.email, " ")
        self.assertEqual(user.password, " ")
        self.assertEqual(user.first_name, " ")
        self.assertEqual(user.last_name, " ")
        self.assertEqual(user.adress, " ")
        self.assertEqual(user.city, " ")
        self.assertEqual(user.zip_code, " ")
        self.assertEqual(user.phone_number, " ")
        self.assertEqual(user.email_is_verified, False)
        self.assertEqual(user.role, "user")
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.is_staff, False)
        self.assertEqual(user.is_superuser, False)
        self.assertEqual(user.last_login, None)

    def test_custom_user_email(self):
        user = CustomUser.objects.get(email=" ")
        self.assertEqual(user.email, " ")
        self.assertNotEqual(user.email, "email")
        self.assertNotEqual(user.email, "email@")
        self.assertNotEqual(user.email, "email@.")
        self.assertNotEqual(user.email, "email@.c")
        self.assertNotEqual(user.email, "email@.co")
        self.assertNotEqual(user.email, "email@.com")

    def test_custom_user_password(self):
        user = CustomUser.objects.get(email=" ")
        self.assertEqual(user.password, " ")
        self.assertNotEqual(user.password, "password")