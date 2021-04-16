from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'A Package which helps in easing your automations involving whatsapp'
LONG_DESCRIPTION = 'This package mainly contains 4 types of senders (text,image/video, audio, document) and 2 ' \
                   'features spam_bot and group_creator '

# Setting up
setup(
    name="autowhat",
    version=VERSION,
    author="Giri",
    author_email="<karnatisaivenkatagiri@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['gTTS', 'Selenium'],

    keywords=['python', 'first package'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
