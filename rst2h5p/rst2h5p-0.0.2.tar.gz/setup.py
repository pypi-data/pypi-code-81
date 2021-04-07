from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.rst').read_text(encoding='utf-8')

setup(
    name='rst2h5p',
    description="Generate HTML5 Packages (H5P) from reStructuredText",
    packages=["rst2h5p"],
    use_scm_version={
        "relative_to": __file__,
        "write_to": "rst2h5p/version.py",
    },
    long_description=long_description,
    url='https://github.com/wallento/rst2h5p',
    author="Stefan Wallentowitz",
    author_email='stefan.wallentowitz@hm.edu',
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Utilities",
        "Topic :: Documentation",
        "Topic :: Text Processing",
        "Topic :: Text Processing :: Markup :: reStructuredText",
    ],
    entry_points={"console_scripts": ["rst2h5p = rst2h5p.main:main"]},
    setup_requires=[
        "setuptools_scm",
    ],
    install_requires=[
        "docutils",
        "pygments"
    ]
)
