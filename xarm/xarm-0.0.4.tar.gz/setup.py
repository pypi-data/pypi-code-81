import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xarm", # Replace with your own username
    version="0.0.4",
    author="Chris Courson",
    author_email="chris@chrisbot.com",
    description="Servo controller to manipulate xArm and LeArm",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ccourson/xArmServoController",
    project_urls={
        "Bug Tracker": "https://github.com/ccourson/xArmServoController/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
