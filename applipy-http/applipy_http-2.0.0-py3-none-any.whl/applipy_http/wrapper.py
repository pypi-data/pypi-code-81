from applipy_http.types import EndpointMethod


class EndpointWrapper:

    def wrap(self, method: str, path: str, handler: EndpointMethod) -> EndpointMethod:
        raise NotImplementedError("Not Implemented")

    def priority(self) -> int:
        """
        The priority defines when the wrapper is applied relative to other
        registered wrappers.
        The highest the priority, the later it is applied (It will wrap all the
        lower priority wrappers)
        """
        return 0
