class InOutSerializerMixin:
    """ Mixin with support for different serializer for GET and POST/PATCH/PUT"""

    input_serializer_class = None
    output_serializer_class = None

    def get_serializer_class(self):
        # noinspection Assert
        assert not any(
            [self.input_serializer_class is None, self.output_serializer_class is None]
        ), "input_serializer_class, output_serializer_class has to be set "

        if str(self.request.method).lower() in ["get"]:
            return self.output_serializer_class

        return self.input_serializer_class


class InOutViewSetMixin:
    """ Viewset Mixin with support for different serializer for GET and POST/PATCH/PUT"""

    input_serializer_class = None
    output_serializer_class = None

    list_serializer_class = None
    detail_input_serializer_class = None
    detail_output_serializer_class = None

    def get_serializer_class(self):
        # noinspection Assert
        assert not any(
            [self.input_serializer_class is None, self.output_serializer_class is None]
        ), "input_serializer_class, output_serializer_class has to be set "

        if str(self.request.method).lower() in ["get"]:
            return self.output_serializer_class

        return self.input_serializer_class
