import io
import os
import pathlib
import re
from os.path import dirname
from os.path import join
from warnings import warn

from setuptools import setup, find_packages, Extension

from src.py_pal import __version__


def read(*names, **kwargs):
    with io.open(
            join(dirname(__file__), *names),
            encoding=kwargs.get('encoding', 'utf8')
    ) as fh:
        return fh.read()


try:
    # Allow installing package without any Cython available. This
    # assumes you are going to include the .c files in your sdist.
    import Cython
except ImportError:
    Cython = None
    warn("Cython package not available, proceeding with precompiled .c extension files.")

compiler_options = {
    'language_level': '3str',
    'embedsignature': True,
}
macros = []
env_trace = os.environ.get('PYPAL_TRACE')
if env_trace:
    # Add directives for Cython code coverage
    compiler_options.update({'linetrace': True})
    macros = [('CYTHON_TRACE', '1')]
    warn("Line coverage analysis for Cython modules enabled.")
else:
    compiler_options.update({
        'boundscheck': False,
        'wraparound': False,
        'infer_types': True,
    })

ext_kwargs = dict(
    define_macros=macros,
)
ext = '.pyx' if Cython else '.c'
extensions = [
    Extension(
        'py_pal.tracer',
        ['src/py_pal/tracer' + ext, 'src/frame/frame.c'],
        include_dirs=['src/frame/'],
        **ext_kwargs
    ),
    Extension(
        'py_pal.metric',
        ['src/py_pal/metric' + ext],
        **ext_kwargs
    ),
    Extension(
        'py_pal.opcode_metric',
        ['src/py_pal/opcode_metric' + ext, 'src/frame/frame.c'],
        include_dirs=['src/frame/'],
        **ext_kwargs
    ),
]

if Cython:
    from Cython.Build import cythonize

    extensions = cythonize(
        extensions,
        compiler_directives=compiler_options,
        force=True if env_trace else False
    )

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# This call to setup() does all the work
setup(
    name='py-pal',
    version=__version__,
    description='Estimate Asymptotic Runtime Complexity from Bytecode executions',
    long_description='%s\n%s' % (
        re.compile('^.. start-badges.*^.. end-badges', re.M | re.S).sub('', read('README.rst')),
        read('CHANGELOG.rst')
    ),
    long_description_content_type='text/x-rst',
    url='https://gitlab.lukasjung.de/root/py-pal',
    project_urls={
        "Documentation": "https://py-pal.readthedocs.io/en/latest/",
    },
    author='Lukas Jung',
    author_email='mail@lukasjung.de',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Utilities',
        'Topic :: Software Development :: Debuggers',
    ],
    python_requires='>=3.7',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'pandas>=1.0,<1.3',
        'numpy>=1.16,<1.21',
        'matplotlib>=3.1,<3.5'
    ],
    entry_points={
        'console_scripts': [
            'pypal=py_pal.__main__:main',
            'py-pal=py_pal.__main__:main',
            'py_pal=py_pal.__main__:main',
        ]
    },
    setup_requires=[
        'cython>=0.29,<0.30',
    ] if Cython else [],
    ext_modules=extensions
)
