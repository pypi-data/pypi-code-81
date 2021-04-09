from setuptools import find_packages, setup

setup(
    name="ken_perlin_noise",
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3',
    url="https://github.com/EgorVoron/py-perlin-noise",
    author="EgorVoron",
    license="MIT",
    install_requires=[
        "numpy>=1.15"
    ],
    zip_safe=False
)
