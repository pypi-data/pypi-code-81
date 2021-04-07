from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from graphene import relay, List
from graphql_relay import from_global_id, to_global_id

from uw_graphene.errors import (
    handle_mutation_errors,
    MutationErrorHandler,
    InvalidGlobalIdError,
    InstanceNotFoundError,
)


def global_id_to_id(global_id, field=None):
    """Method to convert a global id into an id"""
    try:
        return from_global_id(global_id)[1]
    except (UnicodeDecodeError, ValueError):
        raise InvalidGlobalIdError(field, global_id)


def global_id_to_instance(global_id, model_class, field=None, **kwargs):
    """Method to convert a global id to the related instance"""
    try:
        return model_class.objects.get(
            pk=global_id_to_id(global_id, field=field), **kwargs
        )
    except model_class.DoesNotExist:
        raise InstanceNotFoundError(field, global_id)


def id_to_instance(id, model_class, field=None, **kwargs):
    try:
        return model_class.objects.get(pk=id, **kwargs)
    except model_class.DoesNotExist:
        global_id = to_global_id(model_class.__name__, id)
        raise InstanceNotFoundError(field, global_id)


class GlobalIDConverter:
    """Convert input global ids to model ids"""

    @staticmethod
    def is_global_id(key):
        return key == "id" or key[-3:] == "_id"

    @staticmethod
    def get_full_path(path, field):
        full_path_list = path.split('.')
        full_path_list.append(field)
        if '' in full_path_list:
            full_path_list.remove('')
        return '.'.join(full_path_list)

    @classmethod
    def _convert_value(cls, key, value, path=""):
        clean_value = value
        full_path = cls.get_full_path(path, key)
        if isinstance(value, list):
            if len(value) == 0:
                clean_value = value
            elif isinstance(value[0], dict):
                clean_value = [
                    cls.convert_input(nested_value, full_path) for nested_value in value
                ]
            else:
                clean_value = [
                    global_id_to_id(nested_value, field=full_path) for nested_value in value
                ]
        elif isinstance(value, dict):
            clean_value = cls.convert_input(value, full_path)
        elif cls.is_global_id(key):
            clean_value = global_id_to_id(value, field=full_path)
        return clean_value

    @classmethod
    def convert_input(cls, input_val, full_path=""):
        dictionary = {}
        for key, value in input_val.items():
            value = cls._convert_value(key, value, full_path)
            dictionary[key] = value
        return dictionary


class GlobalIDMutation(relay.ClientIDMutation):
    """
    Mixin to parse global_ids of mutations

    Provide a map 'fields_to_model' of field keys (without _id) to ModelClasses
    to get the instance of the id provided on global_id fields

    """

    fields_to_model = {}
    errors = List(MutationErrorHandler.ErrorObjectType)

    class Meta:
        abstract = True

    @classmethod
    def _get_resolver_name(cls, nested_path, key):
        combined_nested_path = cls._combine_nested_path(nested_path, key)
        resolver_name = f"resolve_{combined_nested_path}"
        if hasattr(cls, resolver_name):
            return getattr(cls, resolver_name)
        return None

    @classmethod
    def _get_instance_key(cls, key):
        if key == "id":
            return "_instance"
        if key[-3:] == "_id":
            return key[:-3]
        return key

    @classmethod
    def _combine_nested_path(cls, nested_path, key):
        return f"{nested_path}__{key}" if nested_path else f"{key}"

    @classmethod
    def _get_instance(
        cls,
        key,
        value,
        info,
        nested_path=None,
        fields_to_model={},
        parent={},
        siblings={},
    ):
        method_resolver = cls._get_resolver_name(nested_path, key)
        if method_resolver:
            # method resolver was provided
            try:
                return method_resolver(value, info, parent=parent, siblings=siblings)
            except ObjectDoesNotExist:
                raise InstanceNotFoundError(key)

        if key == "id" and nested_path is not None:
            # don't fetch instances of nested 'id' keys
            return value

        full_nested_path = cls._combine_nested_path(nested_path, key)
        field_to_model = fields_to_model.get(full_nested_path)

        if field_to_model:
            # detailed field_to_model was provided
            model_class = field_to_model
            kwargs = {}
            if isinstance(field_to_model, (list, tuple)):
                model_class, kwargs = field_to_model
            return id_to_instance(value, model_class, field=key, **kwargs)

        field_to_model = fields_to_model.get(key)
        if field_to_model:
            # generic field_to_model was provided
            model_class = field_to_model
            kwargs = {}
            if isinstance(field_to_model, (list, tuple)):
                model_class, kwargs = field_to_model
            return id_to_instance(value, model_class, field=key, **kwargs)

        return value

    @classmethod
    def _fetch_instances(
        cls, values, info, fields_to_model={}, nested_path=None, parent={}
    ):
        nested_lists = {}
        id_lists = {}
        nested_dicts = {}
        instances = {}
        clean_values = {}
        # split values in possible combinations
        for key, value in values.items():
            if isinstance(value, list):
                if value and isinstance(value[0], dict):
                    nested_lists[key] = value
                else:
                    id_lists[key] = value
            elif isinstance(value, dict):
                nested_dicts[key] = value
            elif GlobalIDConverter.is_global_id(key):
                instances[key] = value
            else:
                clean_values[key] = value

        for key, value in instances.items():
            # The order in wich the fields have on the Mutation input
            # determines the order in wich the instances are resolved.
            # If a sibiling is needed in order to resolve another
            # it should be placed first
            clean_value = cls._get_instance(
                key,
                value,
                info,
                parent=parent,
                nested_path=nested_path,
                fields_to_model=fields_to_model,
                siblings=clean_values,
            )
            clean_key = key
            if clean_value is not None:
                clean_key = cls._get_instance_key(key)
            clean_values[clean_key] = clean_value

        for key, value in id_lists.items():
            clean_values[key] = [
                cls._get_instance(
                    key,
                    i,
                    info,
                    parent=parent,
                    nested_path=nested_path,
                    fields_to_model=fields_to_model,
                    siblings=clean_values,
                )
                for i in value
            ]

        for key, value in nested_lists.items():
            new_nested_path = cls._combine_nested_path(nested_path, key)
            clean_values[key] = [
                cls._fetch_instances(
                    nested_value, info, fields_to_model, new_nested_path, clean_values
                )
                for nested_value in value
            ]

        for key, value in nested_dicts.items():
            new_nested_path = cls._combine_nested_path(nested_path, key)
            clean_values[key] = cls._fetch_instances(
                value, info, fields_to_model, new_nested_path, clean_values
            )

        return clean_values

    @classmethod
    def _set_nullable_fields_to_none(cls, values):
        """
        Set fields with kwargs (set_none: True) to none when they are not provided
        """
        input_keys = cls._meta.arguments["input"]._meta.fields.keys()

        nullified_values = dict(values)
        for input_key in input_keys:
            if input_key not in values:
                input_field = getattr(cls._meta.arguments["input"], input_key)
                if input_field and "set_none" in input_field.kwargs:
                    nullified_values[input_key] = None

        return nullified_values

    @classmethod
    def update_instance(cls, instance, values):
        """Use this method to update an instance from the dict input"""
        for attr, value in values.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    @classmethod
    def get_fields_to_model(cls, root, info, input):
        """
        Method to add aditional fields to fields_to_model_mapping
        ex: use this to add 'id' when needed (ex: update mutations)
        """
        return cls.fields_to_model

    @classmethod
    @transaction.atomic
    @handle_mutation_errors
    def mutate(cls, root, info, input):
        fields_to_model = cls.get_fields_to_model(root, info, input)

        nullified_values = cls._set_nullable_fields_to_none(input)
        converted_values = GlobalIDConverter.convert_input(nullified_values)
        values_with_instances = cls._fetch_instances(
            converted_values, info, fields_to_model
        )
        return super().mutate(root, info, values_with_instances)
