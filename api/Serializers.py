from rest_framework import serializers, fields
from administrator import models
from .models import UserToken
from django.utils.timezone import now


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'


class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Season
        fields = '__all__'


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Banner
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
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


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.District
        fields = '__all__'


class DivisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Division
        fields = '__all__'


class ParishSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Parish
        fields = '__all__'


class VillageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Village
        fields = '__all__'


class StreetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Street
        fields = '__all__'
