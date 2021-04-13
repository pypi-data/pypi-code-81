from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.contrib.auth import get_user_model

class GenericUserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user

    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'style',
        )

        validators = [
            UniqueTogetherValidator(
                queryset=get_user_model().objects.all(),
                fields=['username', 'email']
            )
        ]
