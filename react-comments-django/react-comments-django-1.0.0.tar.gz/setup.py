#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys
# from shutil import rmtree

try:
    from setuptools import setup, Command
except ImportError:
    from distutils.core import setup, Command

_here = os.path.dirname(__file__)
about = {}  # type: ignore


def get_version(*file_paths):
    """Retrieves the version from ./__init__.py"""
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


version = '1.0.0'


if sys.argv[-1] == 'publish':
    try:
        import wheel
        print("Wheel version: ", wheel.__version__)
    except ImportError:
        print('Wheel library missing. Please run "pip install wheel"')
        sys.exit()
    os.system('python setup.py sdist bdist_wheel')
    os.system('twine check dist/*')
    os.system('twine upload dist/*')
    # os.system('twine upload --repository-url https://test.pypi.org/legacy/ dist/*')
    sys.exit()

if sys.argv[-1] == 'tag':
    print("Tagging the version on git:")
    os.system("git tag -a %s -m 'version %s'" % (version, version))
    os.system("git push --tags")
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')


# class UploadCommand(Command):
#     """Support setup.py upload."""
#
#     description = "Build and publish the package."
#     user_options = []  # type: ignore
#
#     @staticmethod
#     def status(s):
#         """Prints things in bold."""
#         print("\033[1m{0}\033[0m".format(s))
#
#     def initialize_options(self):
#         pass
#
#     def finalize_options(self):
#         pass
#
#     def run(self):
#         try:
#             self.status("Removing previous builds…")
#             rmtree(os.path.join(_here, "dist"))
#         except OSError:
#             pass
#
#         self.status("Building Source and Wheel (universal) distribution…")
#         os.system("{0} setup.py sdist bdist_wheel --universal".format(sys.executable))
#
#         self.status("Checking packages")
#         os.system("twine check dist/*")
#
#         self.status("Uploading the package to PyPI via Twine…")
#         os.system("twine upload dist/*")
#
#         # self.status("Pushing git tags…")
#         # os.system("git tag v{0}".format(about["__version__"]))
#         # os.system("git push --tags")
#
#         sys.exit()

setup(
    name='react-comments-django',
    version=version,
    description="""React Django forum/comments application with Reddit like features""",
    long_description=readme + '\n\n' + history,
    long_description_content_type="text/x-rst",
    author='studyhub.co',
    author_email='nscozzaro@gmail.com',
    url='https://github.com/studyhub-co/react-comments-django',
    packages=[
        'react_comments_django',
    ],
    include_package_data=True,
    install_requires=["django-crispy-forms>=1.6.1",
                      "django-mptt>=0.8.7",
                      "awesome-slugify>=1.6.5",
                      "django-ipware>=2.1.0",
                      "django-meta>=1.4.1"
                      ],
    license="Apache Software License 2.0",
    zip_safe=False,
    keywords='react-comments-django',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    # # $ setup.py upload support.
    # cmdclass={"upload": UploadCommand},
)
