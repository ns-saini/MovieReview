from rest_framework import serializers
from .models import *


class BasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Basic
        fields = '__all__'


class NamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Names
        fields = '__all__'


class PrincipalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Principal
        fields = '__all__'


class RatingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ratings
        fields = '__all__'


class TitleToNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = TitleToName
        fields = '__all__'
