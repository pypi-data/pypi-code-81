import setuptools

__version__ = "0.3.0b"

with open("README.md", "r") as fh:
    long_description = fh.read()

requires = [
    "dotmap==1.3.23",
    "flake8==3.9.0",
    "pyglet==1.5.15",
    "Shapely==1.7.1"
]

test_requires = [
    "pytest==6.1.2",
    "pytest-cov==2.10.1",
    "mock==4.0.2",
]

setuptools.setup(
    name="car_racer",
    version=__version__,
    author="Joshua Hercher",
    author_email="josh@bitperfect.at",
    description="A small racing game with the possibility to train an AI to learn to play the game",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kamejosh/car_racer",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
    ],
    install_requires=requires,
    extras_require={"testing": test_requires},
    entry_points={
        'console_scripts': [
            'cr_race = car_racer.__init__:race',
            'cr_replay = car_racer.__init__:replay',
        ]
    },
    python_requires='>=3.6',
)