from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='rattools',
    url='https://github.com/jladan/package_demo',
    author='Ldog',
    author_email='ldomgut@protonmail.com',
    # Needed to actually package something
    packages=['rattools'],
    # Needed for dependencies
    install_requires=["pandas","finviz","sklearn","matplotlib"],
    # *strongly* suggested for sharing
    version='0.0.3',
    # The license can be anything you like
    license='MIT',
    description='An example of a python package from pre-existing code',
    # We will also need a readme eventually (there will be a warning)
    # long_description=open('README.txt').read(),
)