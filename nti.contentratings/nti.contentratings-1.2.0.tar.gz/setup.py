import os

from setuptools import setup
from setuptools import find_packages


def read(*rnames):
    with open(os.path.join(os.path.dirname(__file__), *rnames), 'rb') as f:
        data = f.read()
        text = data.decode('utf-8')
    return text


description = read('README.rst') + '\n\n' + \
    '.. rubric:: Detailed Documentation\n\n' + \
    read('src', 'contentratings', 'README.rst') + '\n\n' + \
    read('CHANGES.rst')


setup(
    name='nti.contentratings',
    version='1.2.0',
    description="A small Zope 3 package (which also works with Zope 2.10+ and Five) that allows you to attach ratings to content.",
    long_description=description,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Framework :: Zope3',
        'Framework :: Zope2',
        'Framework :: Plone',
        'Framework :: Plone :: 4.0',
        'Framework :: Plone :: 4.1',
        'Framework :: Plone :: 4.2',
        'Framework :: Plone :: 4.3',
        'Framework :: Plone :: 5.0',
        'Framework :: Plone :: 5.1',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='ratings zope plone zope3',
    author='Alec Mitchell',
    author_email='apm13@columbia.edu',
    url='https://github.com/NextThought/nti.contentratings',
    license='ZPL',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'zope.component >= 5',
        'zope.componentvocabulary',
        'zope.container',
        'BTrees',
        'zope.lifecycleevent',
        'persistent',
        'zope.schema',
        'zope.traversing',
        'zope.deferredimport',
        'zope.annotation',
        'zope.configuration',
        'zope.tales',
        'Acquisition',
    ],
    extras_require={
        'test': [
            'zope.testing',
            'zope.testrunner',
            'zope.app.testing',
            'coverage',
        ],
        'zope3': [
            'zope.app.content',
        ],
    },
)
