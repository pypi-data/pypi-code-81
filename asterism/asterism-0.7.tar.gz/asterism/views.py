from rest_framework.response import Response
from rest_framework.views import APIView


def prepare_response(data):
    """
    Transforms a string, Exception or tuple to consistently structured output.
    """
    data = data.args if isinstance(data, Exception) else data
    if isinstance(data, str):
        detail = data
        objects = []
    else:
        detail = str(data[0])
        objects = data[1] if len(data) > 1 else []
    if objects and not isinstance(objects, list):
        objects = [objects]
    count = len(objects) if objects else 0
    return {"detail": detail, "objects": objects, "count": count}


class BaseServiceView(APIView):
    """Base view which accepts a POST request and returns either 200 OK or
    500 Internal Server Error. Requires child classes to implement a
    `get_service_response()` method."""

    def post(self, request, format=None):
        try:
            response = self.get_service_response(request)
            return Response(prepare_response(response), status=200)
        except Exception as e:
            return Response(prepare_response(e), status=500)


class RoutineView(BaseServiceView):
    """Base view for routines which expose a `run` method which executes the
    main logic."""

    def get_service_response(self, request):
        return self.routine().run()
