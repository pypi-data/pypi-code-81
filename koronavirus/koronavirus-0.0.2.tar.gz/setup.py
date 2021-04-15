from setuptools import setup, find_packages

classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "Topic :: Software Development :: Build Tools",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
]

setup(
    name="koronavirus",
    packages=find_packages(),
    version="0.0.2",
    license="MIT",
    description="Koronavirüs (Covid-19) verilerine erişmenizi sağlayan bir Python modülü.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Dorukyum",
    author_email="dorukyum@gmail.com",
    url="https://github.com/Dorukyum/koronavirus",
    keywords="API, Türkçe, Covid, Korona, Corona",
    install_requires=["requests", "aiohttp"],
    classifiers=classifiers,
)
