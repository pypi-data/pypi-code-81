import os
from .presets import DJANGO_PROJECT_CREATE_COMMAND

def create_django_project(name):
    os.system(DJANGO_PROJECT_CREATE_COMMAND.format(name=name))