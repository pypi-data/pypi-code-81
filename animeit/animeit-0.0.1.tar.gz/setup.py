import setuptools

setuptools.setup(
    name="animeit", # Replace with your own username
    version="0.0.1",
    author="MainKronos",
    author_email="lorenzo.chesi@live.it",
    description="AnimeIT-API",
    long_description="Libreria per accedere facilmente ai dati di vari siti streaming di anime sub ita",
    long_description_content_type="text/markdown",
    url="https://github.com/MainKronos/AnimeIT-API",
    packages=setuptools.find_packages(),
    install_requires=['requests', 'youtube_dl', 'beautifulsoup4'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)