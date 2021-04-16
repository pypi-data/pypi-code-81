import setuptools

setuptools.setup(
    name="mesibo", 
    version="0.0.1",
    author="Mesibo",
    author_email="support@mesibo.com",
    description="This is a test release. The complete mesibo python package will be uploaded soon",
    url="https://github.com/mesibo/python",
    project_urls={
        "Bug Tracker": "https://github.com/mesibo/python/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    package_dir={"": "mesibo"},
    python_requires=">=3.6",
)
