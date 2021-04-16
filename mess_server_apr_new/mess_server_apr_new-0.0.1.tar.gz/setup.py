from setuptools import setup, find_packages

setup(name="mess_server_apr_new",
      version="0.0.1",
      description="mess_server_apr_new",
      author="Ivan Ivanov",
      author_email="iv.iv@yandex.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
