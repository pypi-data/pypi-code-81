from setuptools import setup, find_packages

setup(name="samoryad_messeger_server",
      version="0.0.5",
      description="samoryad_messeger_server",
      author="Andrey Samoryadov",
      author_email="samoryadov@yandex.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
