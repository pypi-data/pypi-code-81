#!/usr/bin/env python3
# coding: utf-8
#
# date: 2021.04.09
# author: liuchao


import os
import os.path
import sys
from jinja2 import Template


DOCKERFILE = Template("""FROM python:3.7
WORKDIR /usr/src/app
COPY . .
RUN pip install --no-cache-dir -i https://mirrors.aliyun.com/pypi/simple -r requirements.txt
EXPOSE {{ expose_port }}
CMD [ "gunicorn", "{{ app_name }}.wsgi:application", "-c", "{{ app_name }}/gunicorn_config.py"]""")

class GenDcokerfile(object):
    def __init__(self, expose_port):
        self.expose_port = expose_port
        self.app_name = os.getcwd().split('/')[-1]

    def create(self):
        context = DOCKERFILE.render(expose_port=self.expose_port, app_name=self.app_name)
        print("***Generate dockerfile to {path}***".format(path=os.getcwd()))
        with open('./Dockerfile', mode='w', encoding='utf-8') as template:
            template.write(context)
        print("***Dockerfile generated Complete**")


def run():
    port = input('please input service port: ')
    if not port:
        print('port is not define, please retry input port')
        sys.exit(1)
    obj = GenDcokerfile(port)
    obj.create()

