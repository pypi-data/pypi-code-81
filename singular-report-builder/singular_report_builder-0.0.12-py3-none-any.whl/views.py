import json

from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from django.views.generic.base import View


class ImpressaoRelatorio(View):
    object_list = []
    _kwargs = {}
    titulo = ''
    template_name = ''
    folder = ''
    def get_context_data(self):
        return {
            'object_list': self.object_list,
            'titulo': self.titulo,
            'user': self.request.user
        }

    def post(self, *args, **kwargs):
        self.object_list = json.loads(self.request.POST['queryset'])
        self._kwargs = json.loads(self.request.POST['kwargs'])
        html = HTML(string=render_to_string(f'{self.folder}{self.template_name}', self.get_context_data()),
                    base_url=self.request.build_absolute_uri())
        result = html.write_pdf()

        return HttpResponse(result, content_type='application/pdf')
