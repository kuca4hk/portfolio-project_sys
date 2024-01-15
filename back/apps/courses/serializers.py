from rest_framework import serializers
from .models import Course, Category


class CourseSerializer(serializers.ModelSerializer):
    price_in_czech = serializers.SerializerMethodField(source='price')
    date = serializers.SerializerMethodField(source='created_at')
    update_at = serializers.SerializerMethodField(source='updated_at')
    created_by = serializers.SerializerMethodField(source='created_by')
    category = serializers.SerializerMethodField(source='category')

    class Meta:
        model = Course
        fields = (
        'id', 'created_by', 'users', 'category', 'name', 'description', 'price_in_czech', 'image', 'date', 'update_at',
        'is_active')

    #TODO - funguje protoze urcujuju jaky model, chci a pri serializaci dokazu v obj predat konkretni zaznam v DB
    def get_price_in_czech(self, obj):
        return f"{obj.price} Kč"

    def get_date(self, obj):
        return obj.created_at.strftime("%d.%m.%Y")

    def get_update_at(self, obj):
        return obj.updated_at.strftime("%d.%m.%Y")

    def get_created_by(self, instance):
        return instance.created_by.get_full_name()

    def get_category(self, obj):
        return [i.name for i in obj.category.all()]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CourseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"
        depth = 1


class CourseUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = (
            'category',
            'name',
            'description',
            'price',
            'image',
            'updated_at',
            'is_active',
        )
