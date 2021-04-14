from setuptools import setup

REQUIREMENTS =['chat_downloader', 'click']

CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Internet',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python'
]

setup(
    name='ladyredhood-chats',
    version='0.1.1',
    description='A small script to extract timestamps from youtube chats',
    author='Aurghyadip Kundu',
    author_email='director@webedutech.org',
    license='MIT',
    url='https://github.com/aurghya-0/ladyredhood-chat',
    packages=['chats'],
    classifiers=CLASSIFIERS,
    install_requires=REQUIREMENTS,
    keywords='youtube youtube-chat youtube-timestamp'
)