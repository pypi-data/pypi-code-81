from setuptools import setup

setup(
    name='reactionary',
    version='0.4.1',
    description='Accurately annotate (meta)genomes with MetaCyc reactions.',
    author='Tomer Altman',
    author_email='python@me.tomeraltman.net',
    packages=['reactionary'],
    install_requires=['camelot-frs', 'biopython', 'ete3', 'docopt','schema', 'future', 'sphinx', 'pypandoc', 'rinohtype'], ##,'scikit-learn','scikit-plot','tkinter'],
    scripts=['bin/run-reactionary'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Operating System :: POSIX",
        ],
    url='https://bitbucket.org/tomeraltman/reactionary/',
    include_package_data=True)
