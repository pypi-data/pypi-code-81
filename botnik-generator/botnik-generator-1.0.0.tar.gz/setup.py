import setuptools
import main

with open('README.md', encoding='utf-8') as readme_file:
    long_description = readme_file.read()

setuptools.setup(
    name='botnik-generator',
    version=main.__version__,
    author='JMcB',
    author_email='joel.mcbride1@live.com',
    license='GPLv3',
    description='Create a new Botnik AI predictive keyboard from a youtube playlist by downloading its subtitles.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/JMcB17/botnik-generator',
    py_modules=['main'],
    entry_points={
        'console_scripts': [
            'botnik-generator=main:main'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Development Status :: 4 - Beta',
        'Environment :: Console',
    ],
    python_requires='>=3',
    install_requires=[
        'youtube-dl',
        'beautifulsoup4',
    ]
)
