from setuptools import setup

setup_args = {
    'name':
        'unfolded',
    'version':
        '0.1.0',
    'description':
        'Metapackage for Unfolded\'s public Python packages.',
    'long_description':
        'Metapackage for Unfolded\'s public Python packages.',
    'author':
        'Unfolded',
    'author_email':
        'info@unfolded.ai',
    'py_modules': [],
    'install_requires': ['unfolded.data-sdk', 'unfolded.map-sdk'],
    'license':
        'Proprietary',
    'classifiers': [
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9']}

if __name__ == '__main__':
    setup(**setup_args)
