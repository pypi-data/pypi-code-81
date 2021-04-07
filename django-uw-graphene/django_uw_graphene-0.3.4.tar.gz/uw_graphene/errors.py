import graphene

from django.core.exceptions import ValidationError
from graphql import GraphQLError

from uw_graphene.utils import to_camel_case


class MutationError(Exception):
    def __init__(self, field, message, error=None, message_list=None):
        self.field = field
        self.error = error
        self.message_list = message_list or [message]
        super().__init__(message)


class PasswordValidationError(MutationError):
    def __init__(self, field, error):
        message_list = error.messages
        super().__init__(field, str(message_list), error, message_list)


class InvalidGlobalIdError(MutationError):
    def __init__(self, field, value):
        camel_case_field = to_camel_case(field)
        message = (
            f"field '{camel_case_field}' with value '{value}' is not a valid global_id"
        )
        super().__init__(camel_case_field, message)


class InstanceNotFoundError(MutationError):
    def __init__(self, field, value=None):
        camel_case_field = to_camel_case(field)
        message = (
            f"field '{camel_case_field}' with id '{value}' not found"
            if value
            else f"field '{camel_case_field}' not found"
        )
        super().__init__(camel_case_field, message)


class MutationErrorHandler:
    class ErrorObjectType(graphene.ObjectType):
        field = graphene.String()
        messages = graphene.List(graphene.String)

    @classmethod
    def parse_error(cls, error):
        if isinstance(error, ValidationError):
            errors = []
            for field, validation_errors in error.error_dict.items():
                messages = []
                for e in validation_errors:
                    messages.append(*e.messages)
                errors.append(cls.to_type_dict(field, messages))
            return errors
        if isinstance(error, MutationError):
            return [cls.to_type_dict(error.field, error.message_list)]

        raise GraphQLError(f"Unhandled Error: {error}")

    @classmethod
    def to_type_dict(cls, field, messages):
        return dict(field=to_camel_case(field), messages=messages)


def handle_mutation_errors(mutation):
    def wrapped_mutation(cls, root, info, input):
        try:
            return mutation(cls, root, info, input)
        except (ValidationError, MutationError) as e:
            errors = MutationErrorHandler.parse_error(e)
            return cls(errors=errors)

    return wrapped_mutation


class PermissionDenied(Exception):
    default_message = "You do not have permission to perform this action"

    def __init__(self, message=None):
        if message is None:
            message = self.default_message

        super().__init__(message)
