from setuptools import setup
from axclf._version import __version__

with open('README.md', encoding='utf-8') as fid:
    LONG_DESCRIPTION = fid.read()

setup(
    name='axclf',
    version=__version__,
    author='Roger D. Serwy',
    author_email='roger.serwy@gmail.com',
    license="BSD License",
    keywords="matplotlib",
    url="http://github.com/serwy/axclf",
    packages=['axclf'],
    description='save/restore plot limits',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    platforms=["Windows", "Linux", "Solaris", "Mac OS-X", "Unix"],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License'
    ],
)
