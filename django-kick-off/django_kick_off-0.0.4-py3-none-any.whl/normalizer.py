import re


def project_to_venv(project_name):
    '''Takes a string like "project_name" and convert to "ProjectName", or
    "projectname" to "Projectname"
    '''
    venv_name = ''
    for word in re.findall('[a-zA-Z]+', project_name):
        venv_name += word.title()
    return venv_name
