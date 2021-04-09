from setuptools import setup

with open("README.md", "r", encoding="utf-8") as readme:
    long_description = readme.read()

setup(
    name="graphepp",
    description="A collection of functions for multipartite entanglement purification protocols (EPP) on noisy graph states",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Julius Wallnöfer",
    url="https://github.com/jwallnoefer/graphepp",
    license="MIT",
    license_files=["LICENSE"],
    install_requires=["numpy>=1.19.2"],
    package_dir={"": "src"},
    packages=["graphepp"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Physics",
        "Intended Audience :: Science/Research",
    ],
    keywords=[
        "quantum information",
        "quantum information theory",
        "graph",
        "graph state",
        "entanglement",
        "entanglement purification",
        "entanglement purification protocol",
        "EPP",
        "entanglement distillation",
        "multipartite entanglement",
    ],
    python_requires=">=3.8.5",
    use_scm_version={
        "write_to": "src/graphepp/version.py",
        "local_scheme": "no-local-version",
    },
    setup_requires=["setuptools_scm"],
)
