from __future__ import print_function
from setuptools import setup, find_packages
import os
from os.path import join as pjoin
from distutils import log

from jupyter_packaging import (
    create_cmdclass,
    install_npm,
    ensure_targets,
    combine_commands,
    get_version,
)


here = os.path.dirname(os.path.abspath(__file__))

log.set_verbosity(log.DEBUG)
log.info('setup.py entered')
log.info('$PATH=%s' % os.environ['PATH'])

name = 'jupyterlab_yq_kfidentity'
LONG_DESCRIPTION = 'Reads JWT from Headers.'

# Get jupyterlab_yq_kfidentity version
version = get_version(pjoin(name, '_version.py'))

js_dir = pjoin(here, 'js')

# Representative files that should exist after a successful build
jstargets = [
    pjoin(js_dir, 'dist', 'index.js'),
]

data_files_spec = [
    ('share/jupyter/nbextensions/jupyterlab-yq-kfidentity', 'jupyterlab_yq_kfidentity/nbextension', '*.*'),
    ('share/jupyter/labextensions/jupyterlab-yq-kfidentity', 'jupyterlab_yq_kfidentity/labextension', '**'),
    ('share/jupyter/labextensions/jupyterlab-yq-kfidentity', '.', 'install.json'),
    ('etc/jupyter/nbconfig/notebook.d', '.', 'jupyterlab-yq-kfidentity.json'),
    (
        "etc/jupyter/jupyter_server_config.d",
        "jupyter-config/jupyter_server_config.d",
        "jupyterlab_yq_kfidentity.json",
    ),
    (
        "etc/jupyter/jupyter_notebook_config.d",
        "jupyter-config/jupyter_notebook_config.d",
        "jupyterlab_yq_kfidentity.json",
    ),
]

cmdclass = create_cmdclass('jsdeps', data_files_spec=data_files_spec)
cmdclass['jsdeps'] = combine_commands(
    install_npm(js_dir, npm=['yarn'], build_cmd='build:prod'), ensure_targets(jstargets),
)

setup_args = dict(
    name=name,
    version=version,
    description=LONG_DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    include_package_data=True,
    install_requires=[
        'ipywidgets>=7.6.0',
        'xmltodict==0.12.0',
        'PyJWT>=2.0.1',
    ],
    packages=find_packages(),
    zip_safe=False,
    cmdclass=cmdclass,
    author='Bohdan Astapov',
    author_email='bohdan.astapov@credo.be',
    url='https://github.com/credo/jupyterlab-yq-kfidentity',
    keywords=[
        'ipython',
        'jupyter',
        'widgets',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: IPython',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Multimedia :: Graphics',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)

setup(**setup_args)
