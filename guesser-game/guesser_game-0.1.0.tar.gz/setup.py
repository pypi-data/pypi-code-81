import os
import setuptools


with open(os.path.join(os.path.dirname(__file__), "README.md")) as readme:
    README = readme.read()

setuptools.setup(
      name="guesser_game",
      version="0.1.0",
      author="Wendy Navarrete",
      author_email="navarrete.wen@gmail.com",
      description="An easy funny game, which the computer will guess the number you have in mind",
      long_description=README,
      long_description_content_type="text/markdown",
      url="https://github.com/mwpnava/Python-Code/tree/master/My_own_Python_package",
      classifiers=[
          "Programming Language :: Python :: 3.6",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
          "Intended Audience :: Other Audience",
          "Topic :: Games/Entertainment"
      ],
      python_requires='>=3.6',
      packages = ['guesser_game']
)
