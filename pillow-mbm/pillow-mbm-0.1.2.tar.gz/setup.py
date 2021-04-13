import os.path
from setuptools import setup

project_path = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(project_path, 'pillow_mbm', 'version.py')) as f:
    exec(f.read())

with open(os.path.join(project_path, 'README.md')) as f:
    readme = f.read()

setup(
    name='pillow-mbm',
    description="A pillow plugin that adds support for KSP's MBM textures",
    version=__version__,
    url='https://github.com/drewcassidy/Pillow-mbm',
    author='Andrew Cassidy',
    long_description=readme,
    long_description_content_type='text/markdown',
    python_requires=">=3.7",
    install_requires=['Pillow', 'click'],
    entry_points={
        'console_scripts': ['convert-mbm = pillow_mbm.__main__:convert_mbm']
    },
    package_dir={'': '.'},
    packages=['pillow_mbm'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Games/Entertainment :: Simulation',
        "Topic :: Multimedia :: Graphics",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
    ],
)
