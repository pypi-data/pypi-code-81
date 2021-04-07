from redlink.models import RedlinkDevice
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer


class RedlinkDeviceSerializer(ModelSerializer):
    created = serializers.DateTimeField(required=False)

    class Meta:
        model = RedlinkDevice
        fields = "__all__"
        extra_kwargs = {"id": {"read_only": True, "required": False}}

    def validate(self, attrs):
        self.Meta.model.objects.filter()
        return attrs


class RedlinkCreateDeviceSerializer(ModelSerializer):
    class Meta:
        model = RedlinkDevice
        fields = (
            "registration_id",
            "name",
            "active",
            "type",
        )
