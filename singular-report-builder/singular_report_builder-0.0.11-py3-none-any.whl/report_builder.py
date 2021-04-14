import os
from django.conf import settings


class ReportBuilder:
    web_url = ''
    report_name = None

    def __init__(self, report_name, model):
        self.report_name = report_name
        self.model = model
        print(self.report_name)

    def create_report(self):
        self.create_template()
        self.create_views()
        return self.create_urls()

    def name_to_camel_case(self):
        return ''.join(x for x in self.report_name.title() if not x.isspace())

    def name_to_snake_case(self):
        return '_'.join(self.report_name.lower().split(' '))

    def create_template(self):
        template_folder = settings.TEMPLATES[0]['DIRS'][0]
        web_file = open(f'{template_folder}/{self.model}/{self.name_to_snake_case()}.html', 'w')
        web_file.write('''
        {% extends 'web_template_base.html' %}
        {% load static %}
        ''')
        pdf_file = open(f'{template_folder}/{self.model}/{self.name_to_snake_case()}_pdf.html', 'w')
        pdf_file.write('''
        {% extends 'pdf_template_base.html' %}
        {% load static%}
        ''')
        print('templates created')

    def create_views(self):
        file_path = os.path.join(settings.BASE_DIR, settings.MAIN_APP, 'core', 'views', self.model,f'{self.name_to_snake_case()}.py')
        view_file = open(file_path, 'w')
        view_file.write(
            f"\nclass {self.name_to_camel_case()}(TemplateView):\n"
            f"    template_name = 'reports/{self.name_to_snake_case()}.html'\n"
            f"\n"
            f"    def get_context_data(self, **kwargs):\n" +
            f"        ctx = super({self.name_to_camel_case()}, self).get_context_data(**kwargs)\n"
            f"        ctx['titulo'] = '{self.report_name}'\n"
            f"        ctx['object_list'] = []\n"
            f"        ctx['print_url']=reverse_lazy('{self.name_to_snake_case()}_pdf')\n"
            f"        return ctx\n"
        )

        view_file.write(
            f"\nclass {self.name_to_camel_case()}PDF(ImpressaoRelatorio):\n"
            f"    template_name = '{self.name_to_snake_case()}_pdf.html'\n"
            f"    titulo = '{self.report_name}'"
            f"    folder = '{self.model}/'"
        )
        print('views created')

    def create_urls(self):
        report_url = f'reports/{self.name_to_snake_case()}'
        file_path = os.path.join(settings.BASE_DIR, settings.MAIN_APP, 'urls.py')
        url_file_read = open(file_path, 'r')
        content = url_file_read.read()
        content = content.split('] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)')[0]
        content += f'''
        url(r'{report_url}/',
        login_required({self.name_to_camel_case()}.as_view()),
        name='{self.name_to_snake_case()}'),\n
        url(r'{report_url}_pdf/',
        login_required({self.name_to_camel_case()}PDF.as_view()),
        name='{self.name_to_snake_case()}_pdf'),
        ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
        '''
        url_file_write = open(file_path, 'w')
        url_file_write.write(content)
        print('urls created')
