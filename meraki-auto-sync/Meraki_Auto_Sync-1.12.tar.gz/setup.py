
"""
setup for click
"""
from setuptools import setup,find_packages
req = ['aiohttp','async-timeout','attrs','bcolors',
'certifi','chardet','idna','meraki','multidict','requests',
'typing-extensions','urllib3','yarl','http3','click','pandas',
'tabulate','python-dateutil','automodinit','python-dotenv','wheel']
setup(
    name='Meraki_Auto_Sync',
    version='1.12',
    author='Josh Lipton',
    author_email='joliptn@cisco.com',
    description='CLI Tool To Sync Meraki Network Accross Orginizations based on Tags',
	packages=find_packages(),
    packages_data=['autosync'],
    include_package_data=True,
	install_requires=[req],
    entry_points="""
        [console_scripts]
        autosync=autosync.cli.cli:cli
    """,
)
