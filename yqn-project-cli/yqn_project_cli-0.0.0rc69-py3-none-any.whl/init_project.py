# -*- coding: utf-8 -*-
# Author: ZKH
# Date：2021/3/16
import os
import sys
import json
import shutil
import datetime
import argparse
from string import Template
from termcolor import colored
from yqn_project_cli.utils.handler import auto_view

regen_file_dirs = {
    'project': [
        '$gitignore',
        '$dockerignore',
        '__init__$py',
        'Dockerfile',
        'entrypoint$sh',
        'gunicorn_config$py',
        'gunicorn_config_test$py',
        'model_url_config_local$yml',
        'model_url_config_online$yml',
        'project_config$py',
        'project_config_flask$py',
        'requirements$txt',
        'template_flask$py',
        'template_flask_local$py',
    ],
    'base_dir_files': [
        '$template_config$py',
    ],
    'scheme_dir_files': [
        'config/__init__.py',
    ],
}

pure_schema_dirs = {
    'project': [
        'api',
        'config',
        'rpc',
        'scripts',
        'thirds',
        'utils',
        'outputs',
        'resources',
        'common',
    ],
    'module': '*',
}

template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "template")
project_dir = os.path.join(template_dir, 'project')


# project
def output_gen_files(config):
    project_name, app_id, output_dir = config['app_name'], config['app_id'], config['app_path']
    today = datetime.datetime.now().strftime('%Y%m%d')
    for sub_dir in regen_file_dirs:
        files = regen_file_dirs[sub_dir]
        if sub_dir == 'scheme_dir_files':
            for file in files:
                lines = []
                file_path = os.path.join(output_dir, project_name, file)
                regen_file_r = open(file_path, "r")
                tmp = Template(regen_file_r.read())
                regen_file_r.close()
                regen_file_w = open(file_path, "w")
                lines.append(tmp.safe_substitute(project_name=project_name, today=today, app_id=app_id))
                regen_file_w.writelines(lines)
                regen_file_w.close()

        else:
            for file in files:
                if sub_dir == 'base_dir_files':
                    template_file_path = os.path.join(template_dir, file)
                    target_dir = output_dir

                else:
                    template_file_path = os.path.join(template_dir, sub_dir, file)
                    target_dir = os.path.join(output_dir, project_name)

                lines = []
                out_name = file.replace("template_", project_name + "_").replace("$", ".")
                gen_file_path = os.path.join(target_dir, out_name)
                template_file = open(template_file_path)
                gen_file = open(gen_file_path, "w")
                tmp = Template(template_file.read())
                lines.append(tmp.safe_substitute(project_name=project_name, today=today, app_id=app_id))
                gen_file.writelines(lines)
                template_file.close()
                gen_file.close()

    # save source json-file config to project config dir for add or update later
    # and then out rid of source json-file config
    shutil.copyfile(config['src_config'], os.path.join(output_dir, project_name, 'config/{}.json'.format(project_name)))


def create_project(config):
    for _dir in pure_schema_dirs['project']:
        if _dir not in ['outputs', 'resources']:
            source_path = os.path.join(template_dir, 'project', _dir)
            target_path = os.path.join(config['app_path'], config['app_name'], _dir)
            shutil.copytree(source_path, target_path)
        else:
            os.mkdir(os.path.join(config['app_path'], config['app_name'], _dir))

    output_gen_files(config)

    print(colored('%s created successfully at %s' % (config['app_name'], config['app_path']), 'green'))


def init_project(config):
    auto_view(config, init=True)
    print(colored(
        '%s has inited, you can enter %s, and run: python %s_flask_local.py' %
        (config['app_name'], os.path.join(config['app_path'], config['app_name']), config['app_name']), 'green'))


def parse_json(args):
    conf = json.load(open(args.config, 'rb'))

    if not (conf.get('app_name', False)
            and isinstance(conf['app_name'], str)):
        raise ValueError('%s 中参数 app_name 需为有效非空字符串' % args.config)

    if not (conf.get('app_id', False)
            and str(conf['app_id']).isdigit()):
        raise ValueError('%s 中参数 app_id 需为有效数值字符串' % args.config)

    if not (conf.get('app_path', False)
            and isinstance(conf['app_path'], str)
            and os.path.exists(conf['app_path'])
            and conf['app_path'] == os.path.abspath(conf['app_path'])):
        raise ValueError('%s 中参数 app_path 需为有效完整路径字符串' % args.config)

    # save source json-file config to project config dir for add or update later
    # and then out rid of source json-file config
    conf['src_config'] = args.config

    return conf


def parse_command():
    parser = argparse.ArgumentParser(description='more faster to create project')
    parser.add_argument('-c', '--config', type=str, required=True,
                        help='json-file config absolute path, '
                             'you can reference sample from README.md in installed yqn_project_cli')

    args = parser.parse_args()

    param_str = '\n'.join(['%20s = %s' % (k, v) for k, v in sorted(vars(args).items())])

    print('usage: %s\n%20s   %s\n%s\n%s\n' % (' '.join(sys.argv), 'ARG', 'VALUE', '_' * 50, param_str))

    print(colored('refer to', 'green'),
          colored('README.md', 'red'),
          colored('from yqn_project_cli in installed packages for more usage info', 'green'))

    return args


def main():
    conf = parse_json(parse_command())

    create_project(conf)

    init_project(conf)


def auto_handler():
    conf = parse_json(parse_command())

    auto_view(conf)

    print(colored('%s has updated ...' % conf['app_name'], 'green'))


if __name__ == "__main__":
    main()
