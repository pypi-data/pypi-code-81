from rest_framework import serializers
from rest_framework.relations import RelatedField
from .models import User


class User_Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

