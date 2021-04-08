import uuid
import datetime

from jinja2 import Environment
from jinja2 import FileSystemLoader

def generate(file_in_templates, out_path, template_dir='templates', assets_path_append='', **kwargs):
    """
    Generates necessary file(s)
    :param file_in_templates: template to work with
    :param out_path: output path to save the generated file to
    :param template_dir: templates directory
    :param assets_path_append:
    :param kwargs: variables
    :return: None
    """

    file_loader = FileSystemLoader(template_dir)
    env = Environment(loader=file_loader)
    template = env.get_template(file_in_templates)

    build_id = str(uuid.uuid4())  # to be used

    output = template.render(kwargs, year=datetime.datetime.now().year,
                             build_id=build_id, assets_path_append=assets_path_append)
    print(output, file=open(out_path, 'w+', encoding="utf8"))