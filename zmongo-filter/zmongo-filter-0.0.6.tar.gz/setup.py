from setuptools import find_packages, setup

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='zmongo-filter',
    version='0.0.6',
    author='Luis Meza',
    author_email='luisfernandomeza@hotmail.es',
    description='Mongo Filter for ReferenceField - EmbeddedDocumentField',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    url='https://gitlab.com/Luisff3rnando/mongo-filter',
    platforms=['Any'],
    py_modules=['zmongo'],
    install_requires=['setuptools'],
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.0',
)
