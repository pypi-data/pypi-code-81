import typing

from .endpoint import IEndpointAnnotation


class Security(IEndpointAnnotation):

    def __init__(self, scheme: str = None, scopes: typing.List[str] = None) -> None:
        """
        The *mode* argument is the type of authentication. The *scopes* argument
        is the OpenAPI security scopes.
        """
        self.scheme = scheme
        self.scopes = scopes or []

    def get_spec(self) -> typing.Dict[str, typing.List[str]]:
        """
        Get the OpenAPI specification for the annotation.
        """
        return {
            self.scheme: self.scopes,
        }
