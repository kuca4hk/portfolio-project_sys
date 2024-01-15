from django.contrib import admin
from .models import Course, Category
# Register your models here.


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass