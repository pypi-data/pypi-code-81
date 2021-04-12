import os

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create template cms plugin (folder, empty HTML template, model) in backend/plugins folder with given name'

    def add_arguments(self, parser):
        parser.add_argument('plugin_name', type=str, help="Name for the plugin.")

    def handle(self, *args, **kwargs):
        base_path = os.path.join(os.getcwd())
        if not os.path.exists(os.path.join(base_path, 'backend')):
            self.stdout.write(self.style.ERROR("Folder doesn't exist: <project_root>/backend"))
            return
        if not os.path.exists(os.path.join(base_path, 'backend', 'plugins')):
            self.stdout.write(self.style.ERROR("Folder doesn't exist: <project_root>/backend/plugins"))
            return
        plugin_name = kwargs['plugin_name']
        project_plugins_dir = os.path.join(os.getcwd(), 'backend', 'plugins')
        new_plugin_dir = os.path.join(project_plugins_dir, plugin_name)
        templates_dir = os.path.join(new_plugin_dir, "templates")
        template_dir = os.path.join(templates_dir, plugin_name)
        migrations_dir = os.path.join(new_plugin_dir, "migrations")

        if os.path.exists(new_plugin_dir):
            self.stdout.write(self.style.ERROR("Plugin with name '{}' already exists.".format(plugin_name)))
        else:
            plugin_name_formatted = ""
            for partial_name in plugin_name.split('_'):
                plugin_name_formatted += partial_name.capitalize()
            plugin_class_name = plugin_name_formatted + 'Plugin'
            model_name = plugin_name_formatted + 'PluginModel'
            os.mkdir(new_plugin_dir)
            os.mkdir(templates_dir)
            os.mkdir(template_dir)
            open(template_dir + '/' + plugin_name + '.html', 'a').close()
            os.mkdir(migrations_dir)
            open(new_plugin_dir + '/__init__.py', 'a').close()
            with open(new_plugin_dir + '/cms_plugins.py', 'a') as f:
                f.writelines([
                    'from cms.plugin_base import CMSPluginBase\n',
                    'from cms.plugin_pool import plugin_pool\n',
                    'from django.utils.translation import pgettext\n',
                    '\n',
                    'from backend.plugins.{plugin_name}.models import {model_name}\n'.format(
                        plugin_name=plugin_name, model_name=model_name
                    ),
                    'from backend.plugins.module_name import MODULE_NAME\n',
                    '\n\n',
                    '@plugin_pool.register_plugin\n',
                    'class {}(CMSPluginBase):\n'.format(plugin_class_name),
                    '\tmodel = {}\n'.format(model_name),
                    '\tmodule = MODULE_NAME\n',
                    '\tname = pgettext(\'admin-ui\', "{}")\n'.format(plugin_class_name),
                    '\trender_template = \'{plugin_name}/{plugin_name}.html\'\n'.format(plugin_name=plugin_name),
                    '\t\n',
                    '\tfieldsets = [\n',
                    '\t\t(\n',
                    '\t\t\tNone,\n',
                    '\t\t\t{\n',
                    '\t\t\t\t\'fields\': [],\n',
                    '\t\t\t\t\'description\': pgettext(\'admin-ui\', ""),\n',
                    '\t\t\t},\n',
                    '\t\t)\n',
                    '\t]\n',
                    '\n',
                    '\tdef get_empty_change_form_text(self, obj=None):\n',
                    '\t\t"""\n',
                    '\t\tReturns the text displayed to the user when editing a plugin\n',
                    '\t\tthat requires no configuration.\n',
                    '\t\t"""\n',
                    '\t\treturn pgettext(\'admin-ui\', "There are no settings for this plugin.")\n'])

            with open(new_plugin_dir + '/models.py', 'a') as f:
                f.writelines([
                    'from cms.models import CMSPlugin\n',
                    'from django.db import models\n',
                    'from django.utils.translation import pgettext\n',
                    '\n\n',
                    'class {}(CMSPlugin):\n'.format(model_name),
                    '\tdef __str__(self) -> str:\n',
                    '\t\treturn \'\'\n',
                ])

            self.stdout.write(self.style.SUCCESS("Plugin '{}' successfully created.".format(plugin_name)))
