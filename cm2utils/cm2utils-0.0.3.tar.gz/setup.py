# 다른 곳에서는 pypi 패키지를 참조하는 것이 아니라 파일을 직접 참조하는 경우가 있음.
# 이런 경우에는 ###으로 표시해 두었음.
# 따라서 pypi에 업로드 하기 위해서는 ###으로 주석된 부분을 없애고, 그에 해당하는 부분을 주석처리해서 pypi에 업로드 해야함. 
# 주석처리해야하는 부분은 ### 줄의 아래나 위에 있을 것임.


import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cm2utils", # 폴더명과 동일한 이름
    version="0.0.3",
    author="CM2Lab",
    author_email="s.park@openest.eu",
    description="Some useful util functions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/cm2lab/util_module",
    # ⬇︎ 배포하는 패키지의 다운로드 url을 적어줍니다.
    # ex_ download_url='https://github.com/doorBW/pypi_deploy_test/archive/master.zip',
    download_url='',
    # ⬇︎ 해당 패키지를 사용하기 위해 필요한 패키지를 적어줍니다. ex. install_requires= ['numpy', 'django']
    # 여기에 적어준 패키지는 현재 패키지를 install할때 함께 install됩니다.
    install_requires=[],
    packages=setuptools.find_packages(),
    # 패키지의 키워드를 적습니다.
    keywords=['utils'],
    # ⬇︎ 파이썬 파일이 아닌 다른 파일을 포함시키고 싶다면 package_data에 포함시켜야 합니다.
    # ex) package_data= {'pyquibase' : ['db-connectors/sqlite-jdbc-3.18.0.jar', 'db-connectors/mysql-connector-java-5.1.42-bin.jar', 'liquibase/liquibase.jar' ]},
    package_data= {},
    # ⬇︎ 위의 package_data에 대한 설정을 하였다면 zip_safe설정도 해주어야 합니다. package_data가 있다면 zip_safe는 반드시 False로.
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)