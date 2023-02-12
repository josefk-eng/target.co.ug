from rest_framework import serializers, fields
from administrator.models import Product, Category, Banner, Season
from .models import UserToken
from django.utils.timezone import now


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        fields = '__all__'


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'


class TokenSerializer(serializers.ModelSerializer):
    # token = serializers.CharField(max_length=1000)
    # deviceId = serializers.CharField(max_length=500)
    # dateAdded = fields.DateField(input_formats=['%Y-%m-%dT%H:%M:%S.%fZ'])

    class Meta:
        model = UserToken
        fields = '__all__'

    # def create(self, validated_data):
    #     return UserToken.objects.create(**validated_data)
    def get_dateAdded(self, obj):
        return now()
