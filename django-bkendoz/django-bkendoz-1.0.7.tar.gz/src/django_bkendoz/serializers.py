from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.contrib.auth import get_user_model
from .core import get_global_history_model


class GenericSerializer(serializers.ModelSerializer):
    class Meta:
        model = None
        fields = "__all__"
        depth = 1


class GenericHistorySerializer(serializers.ModelSerializer):
    action = serializers.SerializerMethodField()
    user_link = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    record_link = serializers.SerializerMethodField()
    model_list_link = serializers.SerializerMethodField()
    record = serializers.SerializerMethodField()

    def get_action(self, global_history):
        if global_history.action == "ED":
            return f"""
            <a class="modal-open get-object-changes" href="#" data-url="{global_history.get_absolute_url()}"
            data-modal="#modal-changes"><i class="fas fa-pen hist-edit"></i></a>
            """
        elif global_history.action == "NE":
            return '<i class="fas fa-plus hist-add"></i>'
        elif global_history.action == "DE":
            return '<i class="fas fa-trash hist-del"></i>'

    def get_user_link(self, global_history):
        return global_history.user.to_datatable()

    def get_date(self, global_history):
        return global_history.date.strftime("%Y-%m-%d %H:%M:%S")

    def get_record(self, global_history):
        return global_history.content_object.history_object.name

    def get_record_link(self, global_history):
        if not global_history.action == "DE":
            return global_history.content_object.history_object.to_datatable()
        else:
            return global_history.record_name

    def get_model_list_link(self, global_history):
        return global_history.content_object.history_object.__class__.href_to_datalist()

    class Meta:
        model = get_global_history_model()
        fields = [
            "action",
            "user_link",
            "date",
            "record_link",
            "model_list_link",
            "record",
        ]
        depth = 1


class GenericUserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user

    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "style",
        )

        validators = [
            UniqueTogetherValidator(
                queryset=get_user_model().objects.all(), fields=["username", "email"]
            )
        ]
