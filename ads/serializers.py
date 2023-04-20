from rest_framework import serializers
from rest_framework.relations import SlugRelatedField, PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from users.models import User
from users.serializers import LocationSerializer
from .models import Ad, Category, Selection


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class AdSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    location = serializers.SerializerMethodField()

    class Meta:
        model = Ad
        fields = ['id', 'name', 'author', 'price', 'description', 'is_published', 'category', 'image', 'location']

    def get_location(self, obj):
        return LocationSerializer(obj.author.locations.first()).data


class SelectionSerializer(ModelSerializer):
    items = PrimaryKeyRelatedField(queryset=Ad.objects.all(), many=True, required=False)

    class Meta:
        model = Selection
        fields = '__all__'


class SelectionCreateSerializer(ModelSerializer):
    owner = SlugRelatedField(slug_field="username", read_only=True)

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["owner"] = request.user
        return super().create(validated_data)

    class Meta:
        model = Selection
        fields = "__all__"


class SelectionListSerializer(ModelSerializer):
    class Meta:
        model = Selection
        fields = ['id', 'name']


class SelectionDetailSerializer(ModelSerializer):
    items = AdSerializer(many=True)

    class Meta:
        model = Selection
        fields = '__all__'


