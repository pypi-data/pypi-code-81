import os
import re

from setuptools import setup, find_packages
from imagepro._version import __version__, __author__, __email__

try: # for pip >= 20
    from pip._internal.network.session import PipSession
except ModuleNotFoundError:
    try: # for 20 > pip >= 10
        from pip._internal.download import PipSession
    except ImportError: # for pip <= 9.0.3
        from pip.download import PipSession

try: # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError: # for pip <= 9.0.3
    from pip.req import parse_requirements


def read_requirements_file(path):
    """
    reads requirements.txt file and handles PyPI index URLs

    Args:
        path (str): path to requirements.txt file

    Returns:
        (tuple of lists)
    """
    session = PipSession()
    base_path = os.path.dirname(path)

    # cache dependencies between files
    _cached_links = {}

    def find_extra_url(filename):
        """
        get the --extra-find_extra_url from the file

        Args:
            filename (str): file name

        Returns:
            find_extra_url
        """
        if filename not in _cached_links:
            # look for index urls
            with open(filename, 'r') as f:
                lines = f.read()
            urls = re.findall('^--extra-index-url (.*)$', lines, re.MULTILINE)
            _cached_links[filename] = urls
        return _cached_links[filename]

    requirements = []
    dependency_links = []
    reqs = parse_requirements(path, session=session)
    try:
        for req in reqs:
            requirements.append(str(req.req))
            filename = re.search('-r ([^\s]+)', req.from_path()).group(1)
            os.path.join(base_path, filename)
            urls = find_extra_url(filename)
            for url in urls:
                if not url.endswith('/'):
                    url += '/'
                dependency_links.append(url + req.req.name)
    except AttributeError:
        for req in reqs:
            requirements.append(str(req.requirement))
            # filename = re.search('-r ([^\s]+)', req.from_path()).group(1)
            # os.path.join(base_path, filename)
            urls = find_extra_url(path)
            for url in urls:
                if not url.endswith('/'):
                    url += '/'
                dependency_links.append(url + req.requirement.name)
    return requirements, dependency_links


install_requires, dependency_links = read_requirements_file('requirements.txt')
setup(
    name='imagepro',
    version=__version__,
    description='Image Processing for Smart Seller',
    license='MIT License',
    setup_requires=[],
    install_requires=install_requires,
    dependency_links=dependency_links,
    author=__author__,
    author_email=__email__,
    packages=find_packages(),
    platforms='any',
    include_package_data=True
)
