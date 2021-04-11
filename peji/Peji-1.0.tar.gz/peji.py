##########################################################################
#
# Pēji — static site generator.
# Homepage: https://peji.gch.icu
#
# LICENSE: The Unlicense
#
# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
#
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# For more information, please refer to <http://unlicense.org/>
#
##########################################################################

__version__ = 1.0

import os
import re
import sys
import shutil

import yaml
import click
import jinja2
import pygments
import markdown


config_yaml_template = '''# Site title.
title: My site
# Site meta description.
description: My cool website.
# Site default theme.
theme: default
# Site menu.
menu:
    Home: /
# Markdown extensions.
# See https://python-markdown.github.io/extensions/
markdown_extensions:
    - admonition
    - codehilite
    - extra
    - meta
    - toc
markdown_extension_configs:
    codehilite:
        noclasses: true
        use_pygments: true
        pygments_style: default
'''

base_j2_template = '''<!DOCTYPE html>
<html lang="en" dir="ltr">
    <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width">
    <title>
    {% block title %}{% endblock %}
    </title>
    {% block head %}{% endblock %}
    </head>
<body>
{% if menu %}
<div class="menu">
    <ul>
        {% for link in menu.keys() %}
        <li><a href="{{ menu.get(link) }}">{{ link }}</a></li>
        {% endfor %}
    </ul>
</div>
{% endif %}
{% block content %}
Nothing here.
{% endblock %}
</body>
</html>
'''

index_j2_template = '''{% extends 'base.j2' %}
{% block title %}{{ title }} | {{ site_title }}{% endblock %}
{% block head %}{{ super() }}
    <link rel="stylesheet" href="/themes/{{ theme }}/css/main.css">
    <link rel="shortcut icon" href="/themes/{{ theme }}/images/favicon.ico"
    type="image/x-icon">
{% endblock %}
{% block content %}
    {{ content | safe }}
{% endblock %}
'''

default_main_css = '''body {
    margin: 32px;
    font-size: 16px;
    color: #000000;
    background-color: #ffffff;
}
a,
a:active,
a:visited {
    color: #3f37c9;
    text-decoration: none;
}
a:hover {
    border-bottom: 1px dashed;
}
.menu {
    margin: 18px 0 28px 0;
}
.menu ul {
    padding: 0;
}
.menu ul li {
    margin: 0;
    padding: 0;
    padding-right: 8px;
    display: inline-block;
    list-style: none;
}
.menu ul li::before {
    content: '|';
    position: relative;
    left: -6px;
}
.menu ul li:first-child::before {
    content: none;
}
pre {
    padding: 12px;
    overflow: auto;
}
dt {
    font-weight: bold;
    font-style: italic;
}
dd {
    margin-top: 8px;
    margin-bottom: 12px;
}
details summary {
    cursor: pointer;
    margin-bottom: 16px;
}
.admonition {
    padding: 0 16px;
}
.info {
    color: #055160;
    background-color: #cff4fc;
    border: 1px solid #055160;
}
.note {
    color: #084298;
    background-color: #cfe2ff;
    border: 1px solid #084298;
}
.tip {
    color: #0f5132;
    background-color: #d1e7dd;
    border: 1px solid #0f5132;
}
.warning {
    color: #664d03;
    background-color: #fff3cd;
    border: 1px solid #664d03;
}
.danger {
    color: #842029;
    background-color: #f8d7da;
    border: 1px solid #842029;
}
'''

pages = 'pages'
layouts = 'layouts'
themes = 'themes'

cwd = os.getcwd()

def read_file(filepath: str) -> str:
    try:
        with open(filepath, 'r') as file:
            return file.read()
    except IOError:
        print('Error: cannot read file: {}'.format(filepath))

def write_to_file(filepath: str, data: str):
    try:
        with open(filepath, 'w') as file:
            return file.write(data)
    except IOError:
        print('Error: cannot write to file: {}'.format(filepath))

def get_config() -> dict:
    config = read_file(os.path.join(cwd, 'config.yaml'))
    return yaml.safe_load(config)

def get_markdown_file_list(directory: str) -> list:
    """Return the list of Markdown files from
    directory. Scan subdirectories too.
    """
    file_list = []
    for root, dirs, files in os.walk(directory):
        for name in files:
            if os.path.splitext(name)[1] == '.md':
                file_list.append(os.path.join(root, name))
    return file_list

def get_new_path(build_dir: str, filename: str) -> str:
    """Make dir and return file path. Example:
    Before:
        ./mysite/pages/index.md
        ./mysite/pages/subfilder/index.md
    After:
        ./mysite/build/index.html
        ./mysite/pages/subfilder/index.html
    """
    relpath = os.path.relpath(filename, start = pages)
    if os.path.dirname(relpath):
        os.makedirs(
            os.path.join(build_dir, os.path.dirname(relpath)),
            exist_ok = True
        )
    return os.path.join(
        build_dir,
        os.path.splitext(relpath)[0] + '.html'
    )

def copy_files(source_dir: str, destination_dir: str):
    shutil.copytree(
        source_dir,
        destination_dir,
        ignore = shutil.ignore_patterns('*.md'),
        dirs_exist_ok = True
    )

def parse_page_metadata(text: str) -> dict:
    """Parse metadata from Markdown as YAML or return None.
    """
    # Find first paragraph that starts and ends with '---'.
    pattern = r'\A\s*(^-{3}$)\n((.+\n)+\n*)(^-{3}$)'
    metadata = re.search(pattern, text, re.MULTILINE)
    if metadata:
        metadata = metadata.group().replace('---', '')
        return yaml.safe_load(metadata)
    else:
        return None

def validate_matadata(config: dict, metadata: dict) -> dict:
    meta = {}
    if metadata:
        try:
            meta['title'] = metadata['title']
        except KeyError:
            meta['title'] = ''
        try:
            meta['theme'] = metadata['theme']
        except KeyError:
            meta['theme'] = config['theme']
        try:
            meta['layout'] = metadata['layout']
        except KeyError:
            meta['layout'] = 'index.j2'
        # Validate config meta
        try:
            meta['site_title'] = config['title']
        except KeyError:
            meta['site_title'] = ''
        try:
            meta['description'] = config['description']
        except KeyError:
            meta['description'] = ''
        try:
            meta['menu'] = config['menu']
        except KeyError:
            meta['menu'] = False
        return meta
    else:
        return None

def render_html_from_markdown(config: dict, text: str) -> str:
    html = markdown.Markdown(
        extensions = config['markdown_extensions'],
        extension_configs = config['markdown_extension_configs']
    )
    return html.convert(text)

def render_template(template: str, **kwargs) -> str:
    """Render template from file.
    Usage:
        render_template('index.j2', title = 'My title')
    """
    env = jinja2.Environment(loader = jinja2.FileSystemLoader(layouts))
    return env.get_template(template).render(**kwargs)

def check_site(cwd: str):
    """Check site config existence and exit if not exist."""
    if not os.path.exists(os.path.join(cwd, 'config.yaml')):
        click.echo(
            'Error: No such file: config.yaml\nAre you in site directory?',
            err = True)
        sys.exit(1)
    else:
        return True

def make_site_dirs(site: str):
    default_dirs = [
        'layouts',
        'pages',
        'themes',
        'themes/default/css',
        'themes/default/images',
        'themes/default/js'
    ]
    dirs = [os.path.join(site, dir) for dir in default_dirs]
    for dir in dirs:
        os.makedirs(os.path.join(cwd, dir), exist_ok = True)

def create_site(site: str):
    make_site_dirs(site)
    write_to_file(
        os.path.join(site, 'config.yaml'),
        config_yaml_template
    )
    write_to_file(
        os.path.join(site, 'layouts/base.j2'),
        base_j2_template
    )
    write_to_file(
        os.path.join(site, 'layouts/index.j2'),
        index_j2_template
    )
    write_to_file(
        os.path.join(site, 'themes/default/css/main.css'),
        default_main_css
    )

def build_site(build_dir: str):
    """Render HTML files and place site data to `build_dir`."""
    config = get_config()
    markdown_files = get_markdown_file_list(pages)
    for file in markdown_files:
        text = read_file(file)
        meta = validate_matadata(
            config,
            parse_page_metadata(text)
        )
        if meta:
            md = render_html_from_markdown(config, text)
            html = render_template(
                meta['layout'],
                theme = meta['theme'],
                title = meta['title'],
                site_title = meta['site_title'],
                description = meta['description'],
                menu = meta['menu'],
                content = md
            )
            # Copy (or replace if exists) files to 'build/' dir.
            copy_files(themes, os.path.join(build_dir, themes))
            copy_files(pages, build_dir)
            # Write rendered HTML into file.
            write_to_file(get_new_path(build_dir, file), html)
        else:
            print('Error: Not rendered: No metadata found in: {}'.format(file))

@click.version_option(
    version = __version__,
    prog_name = 'Pēji')
@click.group()
def cli():
    """Static site generator."""
    pass

@cli.command()
@click.argument('site')
def create(site):
    """Create new site."""
    site = os.path.join(cwd, site)
    create_site(site)
    click.echo('Site created: %s' % site)

@cli.command()
@click.option('-d', '--dir', default = './build/', metavar = 'DIR',
    help = 'Set destination directory. Default: ./build')
def build(dir):
    """Render HTML files."""
    check_site(cwd)
    build_site(dir)
    click.echo('Built in: %s' % dir)

if __name__ == '__main__':
    cli()