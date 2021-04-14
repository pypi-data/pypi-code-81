from django.core.management import BaseCommand

from singular_report_builder.report_builder import ReportBuilder


class Command(BaseCommand):
    help = 'Create report'

    def add_arguments(self, parser):
        parser.add_argument('model', nargs='?', type=str)
        parser.add_argument('name', nargs='+', type=str)

    def handle(self, *args, **kwargs):
        model = kwargs['model']
        report_name = ' '.join(kwargs['name'])
        print(report_name)
        try:
            report_builder = ReportBuilder(report_name, model)
            report_builder.create_report()
        except Exception as e:
            print(e)
