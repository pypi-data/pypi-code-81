from pkg_resources import DistributionNotFound
from pkg_resources import get_distribution

try:
    __version__ = get_distribution("pj_scraper").version
except DistributionNotFound:
    from setuptools_scm import get_version

    __version__ = get_version(root="..", relative_to=__file__)
