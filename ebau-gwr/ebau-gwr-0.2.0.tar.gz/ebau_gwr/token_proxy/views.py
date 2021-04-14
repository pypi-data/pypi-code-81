from rest_framework.mixins import CreateModelMixin
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.viewsets import GenericViewSet

from . import models, serializers


class TokenProxyView(CreateModelMixin, GenericViewSet):
    serializer_class = serializers.TokenProxySerializer
    queryset = models.HousingStatCreds.objects.all()
    renderer_classes = (JSONRenderer,)
    parser_classes = (JSONParser,)
