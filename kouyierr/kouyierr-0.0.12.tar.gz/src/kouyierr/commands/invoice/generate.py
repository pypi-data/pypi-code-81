''' Invoice generator module.

    Parameters:
        year (int): Year of the invoice, default=current
        month (int): Month of the invoice, default=current
        company_config (str): Company config file
        invoice_config (str): Invoice config file
        template (str): Template file path
'''
import calendar
import datetime
import logging
import os
import time
import click
from jinja2 import Environment, FileSystemLoader, TemplateError
import pdfkit
from rich import print as rprint
from rich.console import Console
from rich.progress import track
import yaml

from kouyierr.commands import global_options
from kouyierr.utils.helper import Helper


class Generator:
    ''' Invoice generator class '''
    def __init__(self, helper: Helper, company_config: str, invoice_config: str,
                 invoice_id: str, template: str, output_dir: str):
        logging.basicConfig(format='%(message)s')
        logging.getLogger(__package__).setLevel(logging.INFO)
        self._logger = logging.getLogger(__name__)
        self._helper = helper
        self._company_config = company_config
        self._invoice_config = invoice_config
        self._invoice_id = invoice_id
        self._template = template
        self._output_dir = output_dir

    @staticmethod
    def load_config(company_config: str, invoice_config: str, invoice_id: str) -> dict():
        ''' Build dict config based on local YAML files '''
        try:
            global_config = dict()
            global_config['metadata'] = yaml.load(open(company_config), Loader=yaml.FullLoader)
            invoice_config = yaml.load(open(invoice_config), Loader=yaml.FullLoader)
            global_config['metadata']['customer_id'] = invoice_config['customer_id']
            global_config['metadata']['customer_name'] = invoice_config['customer_name']
            global_config['metadata']['customer_address'] = invoice_config['customer_address']
            global_config['invoices'] = list()
            for invoice in invoice_config['invoices']:
                if 'id' not in invoice:
                    # as 'id' is optional, we need to compute it if not specified
                    invoice['id'] = (
                        f"{invoice['year']}{invoice['month']:02d}_"
                        f"{global_config['metadata']['customer_id']}"
                    )
                if invoice_id in (invoice['id'], "all"):
                    # if filter is matched, or 'all', we add node into dict
                    # static tax compute (to avoid Jinja2 complex filter use)
                    invoice['invoice_total_ht'] = 0
                    for invoice_item in invoice['invoice_items']:
                        invoice['invoice_total_ht'] = invoice['invoice_total_ht'] + \
                            (invoice_item['quantity'] * invoice_item['unit_price'])
                    # static items generation, yes we're lazy
                    invoice['title'] = (
                        f"{global_config['metadata']['customer_name']} | "
                        f"{invoice['year']}{invoice['month']:02d}"
                    )
                    if 'day' not in invoice:
                        # 'day' is optional, if not set we retrieve last day of month aka golden day
                        invoice['day'] = calendar.monthrange(invoice['year'], int(invoice['month']))[1]
                    invoice['generated_date'] = f"{invoice['day']:02d}/{invoice['month']:02d}/{invoice['year']}"
                    invoice_due_date = datetime.datetime.strptime(invoice['generated_date'], '%d/%m/%Y') \
                        + datetime.timedelta(days=30)
                    invoice['invoice_due_date'] = (
                        f'{invoice_due_date.day:02d}/{invoice_due_date.month:02d}'
                        f'/{invoice_due_date.year}'
                    )
                    invoice['invoice_type'] = 'Facture'
                    if 'quote' in invoice:
                        if invoice['quote']:
                            invoice['invoice_type'] = 'Devis'
                    global_config['invoices'].append(invoice)
        except TypeError as exception:
            raise f"Error loading invoice file: {exception}"
        return global_config

    def load_template(self, template: str):
        ''' Load Jinja2 template and attach a custom filter for currency format '''
        try:
            template_file = os.path.basename(template)
            template_path = os.path.dirname(template)
            env = Environment(loader=FileSystemLoader(template_path))
            env.filters['format_currency'] = self._helper.format_currency
            return env.get_template(template_file)
        except TemplateError as exception:
            raise exception

    def generate_files(self, metadata: dict, invoice_content: dict, single_mode: bool = True) -> None:
        ''' Will generate HTML and PDF files '''
        config = {**metadata, **invoice_content}
        template = self.load_template(os.path.abspath(self._template))
        output_from_parsed_template = template.render(config)
        html_file_path = os.path.join(os.getcwd(), f"{invoice_content['id']}.html")
        pdf_file_path = os.path.join(os.getcwd(), f"{invoice_content['id']}.pdf")
        pdfkit_options = {
            'quiet': '',
            'print-media-type': None
        }
        with open(html_file_path, "w") as file_stream:
            file_stream.write(output_from_parsed_template)
            if single_mode:
                rprint(f"[blue]HTML file {html_file_path} has been generated![/blue]")
        pdfkit.from_string(
            input=output_from_parsed_template,
            output_path=pdf_file_path,
            options=pdfkit_options
        )
        if single_mode:
            rprint(f"[blue]PDF file {pdf_file_path} has been generated![/blue]")

    def execute(self):
        ''' Main shceduler that will handle files creation tasks '''
        config = self.load_config(
            company_config=os.path.abspath(self._company_config),
            invoice_config=os.path.abspath(self._invoice_config),
            invoice_id=self._invoice_id
        )
        if not config['invoices']:
            raise Exception(f'No invoice found for id: {self._invoice_id}, aborting...')

        start_time = time.time()
        rprint("[bold green]Starting invoice generation[/bold green] lucky :bear: ...")
        rprint("[bold yellow]Following configuration has been loaded:[/bold yellow]")
        console = Console()
        console.log(config)
        if self._invoice_id == "all":
            rprint(f"Running invoice generation in bulk mode, found {len(config['invoices'])} invoices")
            for invoice in track(config['invoices'], description="Processing..."):
                self.generate_files(config['metadata'], invoice, False)
        else:
            rprint(f"Running invoice generation in single mode for invoice {self._invoice_id}")
            self.generate_files(config['metadata'], config['invoices'][0])
        elapsed_time = round(time.time() - start_time, 2)
        rprint(f"[bold green]Invoice generation complete[/bold green] in {elapsed_time}s :thumbs_up:")


@click.command(help='Generate a new invoice based on definition file and company template')
@global_options
@click.option('--company_config', required=True, type=str, help='Company config file')
@click.option('--invoice_config', required=True, type=str, help='Invoice config file')
@click.option('--invoice_id', required=False, type=str, default='all', help='Invoice ID, default=all')
@click.option('--template', required=True, type=str, help='Template file path')
def generate(company_config: str, invoice_config: str, invoice_id: str, template: str, output_dir: str):
    ''' Generate a new invoice based on definition file and company template '''
    Generator(Helper(), company_config, invoice_config, invoice_id, template, output_dir).execute()
