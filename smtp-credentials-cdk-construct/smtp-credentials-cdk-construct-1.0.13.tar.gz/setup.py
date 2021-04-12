import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "smtp-credentials-cdk-construct",
    "version": "1.0.13",
    "description": "A CDK construct that creates SMTP credentials permitting emails to be sent via SES.",
    "license": "MIT",
    "url": "https://github.com/charlesdotfish/smtp-credentials-cdk-construct",
    "long_description_content_type": "text/markdown",
    "author": "Charles Salmon<me@charles.fish>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/charlesdotfish/smtp-credentials-cdk-construct"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "smtp_credentials",
        "smtp_credentials._jsii"
    ],
    "package_data": {
        "smtp_credentials._jsii": [
            "smtp-credentials-cdk-construct@1.0.13.jsii.tgz"
        ],
        "smtp_credentials": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk.aws-iam>=1.97.0, <2.0.0",
        "aws-cdk.aws-lambda>=1.97.0, <2.0.0",
        "aws-cdk.aws-logs>=1.97.0, <2.0.0",
        "aws-cdk.aws-ssm>=1.97.0, <2.0.0",
        "aws-cdk.core>=1.97.0, <2.0.0",
        "aws-cdk.custom-resources>=1.97.0, <2.0.0",
        "constructs>=3.2.27, <4.0.0",
        "jsii>=1.26.0, <2.0.0",
        "publication>=0.0.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
