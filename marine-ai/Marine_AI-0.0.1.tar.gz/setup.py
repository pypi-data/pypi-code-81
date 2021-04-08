import setuptools

setuptools.setup(
    name='Marine_AI',      #库的名字
    version = '0.0.1',     #库的版本号，后续更新的时候只需要改版本号就行了
    anthor = 'Kevin',
    anthor_email = '1595546523@qq.com',
    description="Combination of ocean and deep learning",
    long_description_content_type='text/markdown',
    url="https://github.com/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)