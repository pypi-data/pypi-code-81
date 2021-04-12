from setuptools import setup, find_packages


setup(name='messenger_server_apr_kinder',
      version='0.0.1',
      description='mess_server_Kinder',
      author='Ivan Kinder',
      author_email='example@example.com',
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
