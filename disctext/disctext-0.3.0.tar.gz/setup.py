from setuptools import setup


with open("README.rst", "rb") as file:
    readme = file.read().decode("utf-8")

setup(
    name = "disctext",
    version = "0.3.0",
    packages = ["disctext"],
    author = "Akbar Amin",
    author_email = "akbar.amin917@gmail.com",
    url = "https://github.com/akbar-amin/disctext",
    description = "A simple tool for creating ASCII art and sharing it on Discord.",
    keywords = ["discord", "ascii", "art", "pipeline", "capture"], 
    license="MIT License",
    entry_points = {
        "console_scripts": [
            "disctext=disctext.session:main"
        ]
    },
    install_requires = ["eventkit", "discord.py", "opencv_python", "numpy", "python-dotenv"]
)