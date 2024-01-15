from django.db import models
from ..users.models import CustomUser

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    short_name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Course(models.Model):
    created_by = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, help_text="User who created this course"
    )
    users = models.ManyToManyField(
        CustomUser,
        related_name="courses",
        blank=True,
        help_text="Users who bought this course",
    )
    category = models.ManyToManyField(Category, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()
    image = models.ImageField(upload_to="courses", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

