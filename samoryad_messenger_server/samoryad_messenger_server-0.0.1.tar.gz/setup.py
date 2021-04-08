from setuptools import setup, find_packages

setup(name="samoryad_messenger_server",
      version="0.0.1",
      description="mess_server",
      author="Andrey Samoryadov",
      author_email="samoryadov@yandex.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
