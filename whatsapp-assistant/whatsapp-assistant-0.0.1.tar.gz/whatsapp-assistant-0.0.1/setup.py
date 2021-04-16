from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'A Package which helps in easing your automations involving whatsapp'
LONG_DESCRIPTION = 'This package mainly contains 4 senders(text,image/video, audio, document) and 2 features namely spam_bot and group_creator'

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="whatsapp-assistant",
    version=VERSION,
    author="Giri",
    author_email="<karnatisaivenkatagiri@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['gTTS', 'Selenium'],  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'

    keywords=['python', 'first package'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)