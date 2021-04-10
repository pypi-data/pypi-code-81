import setuptools
import aws_simple_pipeline

setuptools.setup(
    name="aws_simple_pipeline",
    version=aws_simple_pipeline.__version__,
    author=aws_simple_pipeline.__author__,
    author_email="alessandra.bilardi@gmail.com",
    description="A simple AWS CDK Python pipeline",
    long_description=open('README.rst').read(),
    long_description_content_type="text/x-rst",
    url="https://aws-simple-pipeline.readthedocs.io/",
    packages=setuptools.find_packages(),
    install_requires=[
        "aws-cdk.core>=1.62.0,<=1.80.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    project_urls={
        "Source":"https://github.com/bilardi/aws-simple-pipeline",
        "Bug Reports":"https://github.com/bilardi/aws-simple-pipeline/issues",
        "Funding":"https://donate.pypi.org",
    },

)
