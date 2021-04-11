import os
import decimal

from datetime import datetime

from flask import (
    abort,
    Blueprint,
    json,
    render_template,
    request,
    send_from_directory,
    render_template_string
)

from ..form import create_wtform_from_schema
from .utils import (
    get_asset_url,
    get_nexus_projects,
    get_nexus_data,
    store_nexus_data,
    load_json,
    render_nexus,
    render_form,
    PROJECTS_DIR
)

nexus_dev_pages = Blueprint(
    'nexus_dev_pages',
    __name__,
    static_folder=None,
    template_folder=None
)

@nexus_dev_pages.route(f'/{PROJECTS_DIR}/<appname>/assets/<path:filename>')
def asset_file(appname, filename):
    return send_from_directory(f'{PROJECTS_DIR}/{appname}/assets/', filename)

@nexus_dev_pages.route('/')
def dev_home():
    nexus_projects = get_nexus_projects()
    template = ''
    for nexus in nexus_projects:
        template += f'<a href="/{nexus}/">{nexus}</a><br />'
    return render_template_string(template, **{})

@nexus_dev_pages.route('/<nexus_name>/')
def nexus_home(nexus_name):
    html = render_nexus(nexus_name, **{'section': 'render'})
    return html if html else render_template_string('Error', **{})

@nexus_dev_pages.route('/<nexus_name>/form/', methods = ['POST', 'GET'])
def nexus_form(nexus_name):
    now = datetime.now()
    ts = datetime.timestamp(now)
    schema = load_json(f'{PROJECTS_DIR}/{nexus_name}/', 'form.json')
    form_cls = create_wtform_from_schema(schema)
    if request.method == 'POST':
        nexus_form = form_cls(request.form)
        if nexus_form.validate():
            store_nexus_data(nexus_name, nexus_form.data)
        form = nexus_form
    else:
        data = get_nexus_data(nexus_name)
        form = form_cls(**data)

    extra_kwargs = {
        'section': 'form',
        'form_html': render_form(nexus_name, **{'form': form})
    }
    html = render_nexus(nexus_name, **extra_kwargs)
    return html if html else abort(404)
