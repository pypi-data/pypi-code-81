from distutils.core import setup
try:
    import pypandoc
    long_description = pypandoc.convert_file("README.md", "rst")
    print (long_description)
except (IOError, ImportError):
    long_description = open("README.md").read()

setup(
    name='dashcrypt',
    packages=['dashcrypt'],
    version='1.1',
    license='MIT',
    description='Simple Encrypt basic hash',
    long_description=long_description,
    author='Billal Fauzan',
    author_email='billal.xcode@domain.com',
    url='https://github.com/billalxcode/dashcrypt',
    download_url='https://github.com/user/reponame/archive/v_01.tar.gz',
    keywords=['encrypt', 'encode', 'encoder', 'crypto', 'dashcrypt', 'hash'],
    classifiers=[
        'Development Status :: 3 - Alpha',  # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',  # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',  # Again, pick a license
        'Programming Language :: Python :: 3',  #Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
