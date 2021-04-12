from setuptools import setup

setup(name='python-ecb-daily',
      version='0.3',
      description='Python ECB Daily Rates Wrapper',
      url='https://github.com/fatihsucu/python-ecb-daily',
      author='Fatih Sucu',
      author_email='fatihsucu0@gmail.com',
      license='MIT',
      packages=['ecb'],
      install_requires=[
        "feedparser"
      ],
      zip_safe=False
)
