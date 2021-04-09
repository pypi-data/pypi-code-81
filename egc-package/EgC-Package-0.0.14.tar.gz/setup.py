import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
def get_extra_requires(path, add_all=True):
    import re
    from collections import defaultdict

    with open(path) as fp:
        extra_deps = defaultdict(set)
        for k in fp:
            if k.strip() and not k.startswith('#'):
                tags = set()
                if ':' in k:
                    k, v = k.split(':')
                    tags.update(vv.strip() for vv in v.split(','))
                tags.add(re.split('[<=>]', k)[0])
                for t in tags:
                    extra_deps[t].add(k)

        # add tag `all` at the end
        if add_all:
            extra_deps['all'] = set(vv for v in extra_deps.values() for vv in v)

    return extra_deps

setuptools.setup(
    name="EgC-Package", # Replace with your python folder name 
    version="0.0.14",
    install_requires=["requests", "keras"],
    extras_require=get_extra_requires('extra-requirements.txt'),
    author="EGC",# Replace with your own username
    author_email="EGC@example.com",# Replace with your own username
    description="A small example package from EGC",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/EgC-Team/EngineeringGoesCloud",
    #packages=["src","src.demo"],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
