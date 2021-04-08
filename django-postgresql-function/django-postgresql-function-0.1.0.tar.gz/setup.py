import re

from os.path import abspath
from os.path import dirname
from os.path import join

from pkg_resources import Requirement
from setuptools import find_packages
from setuptools import setup


_COMMENT_RE = re.compile(r'(^|\s)+#.*$')


def _get_requirements(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            line = _COMMENT_RE.sub('', line)
            line = line.strip()
            if line.startswith('-r '):
                for req in _get_requirements(
                    join(dirname(abspath(file_path)), line[3:])
                ):
                    yield req
            elif line:
                req = Requirement(line)
                req_str = req.name + str(req.specifier)
                if req.marker:
                    req_str += '; ' + str(req.marker)
                yield req_str


def main():
    setup(
        name='django-postgresql-function',
        version='0.1.0',
        packages=find_packages('src'),
        package_dir={'': 'src'},
        include_package_data=True,
        url='https://github.com/maksimyuk/django-postgresql-function',
        license='MIT',
        author='wgh',
        author_email='maksimyuk.georgiy@gmail.com',
        description='Additional PostgreSQL DataBase Django functions',
        install_requires=tuple(_get_requirements('requirements/base.txt')),
    )


if __name__ == '__main__':
    main()
