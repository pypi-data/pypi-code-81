import os
import sys
import shutil
from setuptools import setup
import pyct.build
import param
import re


version = param.version.get_setup_version(__file__, 'basic_pkg', archive_commit="$Format:%h$")
if version == 'None':
    sys.exit("Param seems to be unable to find the version of your package. Are you sure you tagged it with annotation?")


if 'sdist' in sys.argv and 'bdist_wheel' in sys.argv:
    try:
        version = re.split('((\d+\.)+(\d+[^\.|\+|\s]*))', version)[1]
    except IndexError:
        print("Param can't parse your version correctly; are you sure you entered it as a set of digits separated by commas in the tag?")
        sys.exit(1)


setup_args = dict(
    name='mijn_pkg',
    version=version,
    install_requires=[
        'xarray',
        'pyct >=0.4.8',
        'param'
        ],
    zip_safe=False,
    packages=['basic_pkg',],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'basic_pkg = basic_pkg.__main__:main'
        ]
    }
)


if __name__ == '__main__':
    example_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                'basic_pkg', 'examples')

    if 'develop' not in sys.argv:
        pyct.build.examples(example_path, __file__, force=True)
    setup(**setup_args)

    if os.path.isdir(example_path):
        shutil.rmtree(example_path)