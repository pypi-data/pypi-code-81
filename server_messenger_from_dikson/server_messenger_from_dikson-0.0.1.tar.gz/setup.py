from setuptools import setup, find_packages

setup(name="server_messenger_from_dikson",
      version="0.0.1",
      description="server part of the messenger",
      author="Aleksey Ulyanov",
      author_email="ulyanov-649@yandex.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
