from setuptools import setup

setup(
        name='cryptocurrency-cli-tools',
        version='0.0.5',
        description='CLI commands for common cryptocurrency related operations',
        author='Louis Holbrook',
        author_email='dev@holbrook.no',
        packages=[
            'cryptocurrency_cli_tools.runnable',
            ],
        install_requires=[
            'bip_utils==1.4.0',
            ],
        #scripts=[
        #    'scripts/bip39gen',
        #    ],
        url='https://gitlab.com/nolash/cryptocurrency-cli-tools',
        classifiers=[
            'Programming Language :: Python :: 3',
            'Operating System :: OS Independent',
            'Development Status :: 3 - Alpha',
            'Environment :: Console',
            'Intended Audience :: End Users/Desktop',
            'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
            'Topic :: Utilities',
            ],
        entry_points = {
            'console_scripts': [
                'bip39gen=cryptocurrency_cli_tools.runnable.bip39gen:main',
                ],
            },
        )
        

