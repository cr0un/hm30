from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import Location, User


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['name', 'lat', 'lng']


class UserSerializer(serializers.ModelSerializer):
    locations = LocationSerializer(many=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'role', 'age', 'locations']
        locations = LocationSerializer(many=True)

    def create(self, validated_data):
        locations_data = validated_data.pop('locations')
        password = validated_data.pop('password')

        user = User.objects.create(
            **validated_data,
            password=make_password(password)
        )

        for location_data in locations_data:
            location, _ = Location.objects.get_or_create(**location_data)
            user.locations.add(location)

        user.save()
        return user

    def update(self, instance, validated_data):
        locations_data = validated_data.pop('locations', [])

        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        instance.locations.clear()
        for location_data in locations_data:
            location, _ = Location.objects.get_or_create(**location_data)
            instance.locations.add(location)

        return instance

