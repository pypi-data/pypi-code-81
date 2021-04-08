from setuptools import setup, find_packages

setup(name="samoryad_messenger_client",
      version="0.0.2",
      description="mess_client",
      author="Andrey Samoryadov",
      author_email="samoryadov@yandex.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
