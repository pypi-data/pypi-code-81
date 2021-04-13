import setuptools

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='xyw-utils',
    version='0.0.2',
    author='二炜',
    author_email='1174543101@qq.com',
    description='个人工具合集',
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_package_data=True,
    package_data={
        'xyw_utils': []
    },
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'pandas',
        'numpy',
        'scipy',
        'pygal',
        'cairosvg',
        'cssselect2',
        'pikepdf',
        'img2pdf',
        'openpyxl',
        'xlwt',
        'xlsxwriter',
    ],
)
