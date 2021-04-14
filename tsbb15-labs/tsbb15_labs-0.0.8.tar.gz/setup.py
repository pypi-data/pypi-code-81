import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

def _load_requirements(path_dir = '.', file_name = 'requirements.txt', comment_char = '#'):
    """Load requirements from a file
    >>> _load_requirements(PROJECT_ROOT)  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    ['numpy...', 'torch...', ...]
    """
    with open(os.path.join(path_dir, file_name), 'r') as file:
        lines = [ln.strip() for ln in file.readlines()]
    reqs = []
    for ln in lines:
        # filer all comments
        if comment_char in ln:
            ln = ln[:ln.index(comment_char)].strip()
        # skip directly installed dependencies
        if ln.startswith('http'):
            continue
        if ln:  # if requirement is not empty
            reqs.append(ln)
    return reqs


setuptools.setup(
    name="tsbb15_labs",
    version="0.0.8",
    author="Johan Edstedt",
    author_email="johan.edstedt@liu.se",
    description="Convenience functions for the tsbb15 labs.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Parskatt/tsbb15_labs",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    setup_requires=[],
    install_requires=_load_requirements(),
    python_requires='>=3.6',
    package_data={'tsbb15_labs': ['images/*','images/chessboard/*','images/lab3/*']}
)
