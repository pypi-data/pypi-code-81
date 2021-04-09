from setuptools import setup, find_packages

def parse_requirements(requirement_file):
    with open(requirement_file) as f:
        return f.readlines()

version = dict()
with open("./atomic_red_team/utils/version.py") as fp:
    exec(fp.read(), version)


setup(
    name='atomic-red-team',
    version=version['__version__'],
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='A python package to execute Atomic tests',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    install_requires=parse_requirements('./requirements.txt'),
    keywords=['atomic-red-team', 'att&ck', 'test', 'redcanary', 'mitre', 'executor'],
    url='https://github.com/MSAdministrator/atomic_red_team',
    author='MSAdministrator',
    author_email='rickardja@live.com',
    python_requires='>=3.6, <4',
    entry_points={
          'console_scripts': [
              'atomic-red-team = atomic_red_team.__main__:main'
          ]
    }
)