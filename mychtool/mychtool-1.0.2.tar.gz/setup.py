from setuptools import setup, find_packages
import traceback

try:
    setup(
        name = 'mychtool',
        version = '1.0.2',
        author = 'Zhou Fang',
        author_email = 'thomas.zhouf@hotmail.com',
        description = 'My ClickHouse Tool',
        long_description = open('README.md').read(),
        packages = find_packages(),
        install_requires=[
            "sqlalchemy == 1.3.20",
            "pandas == 1.1.3",
            "clickhouse_driver == 0.2.0",
            "mysql-replication == 0.23",
            "PyMySQL == 0.9.3"
            ],
    )
except:
    traceback.print_exc()
