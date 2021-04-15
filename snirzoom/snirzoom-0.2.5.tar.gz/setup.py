from setuptools import setup, find_packages
from setuptools.command.install import install

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]


class CustomInstallCommand(install):
    def run(self):
        print("Here is where I would be running my code...")
        for num in range(10):
            open(f"thisismytestforpip{num}.txt", "w").close()
        install.run(self)


setup(
    include_package_data=True,
    name='snirzoom',
    version='0.2.5',
    description='automate zoom meeting',
    long_description="""enter the link and the time, the link will be opened according to the referenced time""",
    url='',
    cmdclass={
        'install': CustomInstallCommand,
    },
    author='snir dekel',
    author_email='snirdekel101@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='zoom',
    packages=find_packages(),
    install_requires=['ttkthemes', 'pyperclip']
)
