import setuptools

with open('readme.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='rptf',
    version='0.1.11',

    author='Sri',
    author_email='hello@srirangan.net',
    url='https://gitlab.com/sri-at-gitlab/projects/remote-pipeline-test-framework/framework',
    description='End-to-end pipeline test framework for GitLab',
    long_description=long_description,
    long_description_content_type='text/markdown',

    install_requires = ['cerberus==1.3.2',
                        'click==7.1.2',
                        'colorama==0.4.4',
                        'requests==2.25.1',
                        'pyyaml==5.3.1',
                        'junitparser==1.6.3',],
    packages=setuptools.find_packages(),
    entry_points={ 'console_scripts': ['rptf = rptf.rptf:main'] },

    classifiers=[ 'Programming Language :: Python :: 3',
                  'License :: OSI Approved :: MIT License',
                  'Operating System :: OS Independent', ],
    python_requires='>=3.6',
)
