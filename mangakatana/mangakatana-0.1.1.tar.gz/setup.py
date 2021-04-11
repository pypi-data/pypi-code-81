from setuptools import setup, find_packages


def read_file(file):
	with open(file, "r") as fh:
		return fh.read()


VERSION = "0.1.1"


setup(
	name="mangakatana",
	packages=find_packages(),
	version=VERSION,
	license="MIT",

	description="An API to query the mangatkatana.com site using BeautifulSoup",
	long_description=read_file("README.md"),
	long_description_content_type="text/markdown",

	author="Joshua Nixon",
	author_email="joshuanixonofficial@gmail.com",

	url="https://github.com/nixonjoshua98/mangakatana",

	download_url=f"https://github.com/nixonjoshua98/mangakatana/archive/{VERSION}.tar.gz",

	keywords=["manga", "manganelo", "scrapper", "web", "mangakakalot", "comic", "manhwa", "mangakatana"],

	install_requires=[
		"bs4",
		"requests",
	],

	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
		"Development Status :: 5 - Production/Stable",
		"Intended Audience :: Developers",
		"Topic :: Software Development :: Build Tools",
	],

	python_requires='>=3.7'
)
