from django.db.models import Prefetch
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.renderers import JSONRenderer
from scarlet.pagebuilder.serializers import PageListSerializer, PageSerializer
from . import get_page_model

Page = get_page_model()


class PageListView(ListAPIView):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    renderer_classes = [JSONRenderer]
    pagination_class = None


class PageDetailsView(RetrieveAPIView):
    serializer_class = PageSerializer
    queryset = Page.objects.all()
    renderer_classes = [JSONRenderer]
    lookup_field = "slug"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .prefetch_related(
                "page_hero_modules",
                "page_two_column_modules",
                "page_icon_list_modules",
                "page_header_modules",
                "page_faq_modules",
                "page_location_modules",
                "page_gallery_modules",
                "page_carousel_modules",
            )
        )
