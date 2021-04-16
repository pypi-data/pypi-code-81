from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='skyway',
    version='0.0.1',
    description='Registery For Me',
    long_description=open('README.txt').read() + '\n\n' +
    open('CHANGELOG.txt').read(),
    url='',
    author='IYE',
    author_email='yigitgulay11@outlook.com',
    license='MIT',
    classifiers=classifiers,
    keywords='registery',
    packages=find_packages(),
    install_requires=['']
)
