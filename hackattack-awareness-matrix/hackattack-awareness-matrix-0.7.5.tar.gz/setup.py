from setuptools import find_packages, setup


setup(
    name='hackattack-awareness-matrix',
    version='0.7.5',
    author="Daniel Sternig - HACKATTACK IT Security GmbH",
    author_email="daniel.sternig@hackattack.com",
    description="A packaged web-application that should support users when dealing with awareness-measures in their companies",
    long_description="A packaged web-application that should support users when dealing with awareness-measures in their companies.",
    long_description_content_type="text/markdown",
    url="https://www.hackattack.com/awareness/",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': ['hackattack-awareness-matrix=hackattack_awa_matrix.command_line:main']
    },
    python_requires='>=3.6',
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'python-dateutil',
        'flask',
        'gevent',
        'XlsxWriter'
    ],
)