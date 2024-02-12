from rest_framework import serializers
from .models import Course, Category
from ..users.models import CustomUser


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
        return obj.price

    def get_date(self, obj):
        return obj.created_at.strftime("%d.%m.%Y")

    def get_update_at(self, obj):
        return obj.updated_at.strftime("%d.%m.%Y")

    def get_created_by(self, instance):
        if instance.created_by.get_full_name() == "":
            return instance.created_by.username
        else:
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

    def update(self, instance, validated_data):
        instance.category = validated_data.get('category', instance.category)
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.image = validated_data.get('image', instance.image)
        instance.updated_at = validated_data.get('updated_at', instance.updated_at)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance


class CourseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = (
            'created_by',
            'category',
            'name',
            'description',
            'price',
            'is_active',
        )

    def create(self, validated_data):
        user = CustomUser.objects.get(email=validated_data['created_by'])

        course = Course.objects.create(
            created_by=user,
            name=validated_data['name'],
            description=validated_data['description'],
            price=validated_data['price'],
            is_active=validated_data['is_active'],
        )
        course.category.set(validated_data['category'])
        course.save()
        return course

    def update(self, instance, validated_data):
        instance.created_by = validated_data.get('created_by', instance.created_by)
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.category.set(validated_data['category'])
        instance.save()
        return instance

class CourseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

