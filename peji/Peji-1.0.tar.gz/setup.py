from setuptools import setup


with open("README.md", "r") as long_descr:
    long_description = long_descr.read()

setup(
    name='Peji',
    version='1.0',
    author='gd',
    description='Static site generator.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://peji.gch.icu/',
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: The Unlicense (Unlicense)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=['peji'],
    install_requires = [
        'click>=7.1.2',
        'markdown>=3.3.4',
        'Jinja2>=2.11.3',
        'Pygments>=2.8.1',
        'PyYAML>=5.4.1'
    ],
    entry_points = {
        'console_scripts': [
            'peji = peji:cli'
        ]
    }
)
