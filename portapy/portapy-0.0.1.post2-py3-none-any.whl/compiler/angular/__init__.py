"""
JavaScript/TypeScript compiler for portapy.

This
"""

from distutils.dir_util import copy_tree

from portapy.compiler import *


Manifest(
    Compile('lib/portapy-js', 'portapy.compiler.js'),

    Function(shutil.rmtree, '__pycache__', ignore_errors=True),
    Function(shutil.rmtree, 'node_modules', ignore_errors=True),
    Function(os.unlink, '__init__.py'),

    Shell('npm install'),
    Template(
        'src/lib/portapy-angular.service.ts.jinja',
        'src/lib/portapy-angular.service.ts',
        keep=False,
    ),
    Template(
        'src/lib/portapy-angular.config.ts.jinja',
        'src/lib/portapy-angular.config.ts',
        keep=False,
    ),
    Shell('npm run tsfmt -- -r src/lib/portapy-angular.service.ts'),
    Shell('npm run tsfmt -- -r src/lib/portapy-angular.config.ts'),
    Shell('npm run build'),

    config_vars=['prefix'],
    dist_dir='build/dist/portapy-angular',
)
