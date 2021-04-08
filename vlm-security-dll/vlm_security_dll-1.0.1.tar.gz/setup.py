
import setuptools

with open("README.md", "r",encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vlm_security_dll",
    version="1.0.1",
    author="VLM-Security",
    author_email="service@vlm-security.com",
    description="VLM-Security Python SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/VLM-Security/vlm_security_dll",
    packages=setuptools.find_packages(),
    # pymodules=[
    #    "vlm-security-dll"
    # ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
)
