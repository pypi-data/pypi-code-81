from setuptools import setup,find_packages

with open("README.md", encoding='utf-8') as fh:
    long_d = fh.read()


setup(name='gameturtle',
      long_description_content_type="text/markdown",
      version = '0.25',
      description = 'Python gameturtle Module for make animations and games easily，by www.lixingqiu.com ',
      long_description = long_d,      
      keywords = 'turtle game tkinter game pillow numpy pixel collide',
      url = 'http://www.lixingqiu.com',
      author ='lixingqiu',
      author_email = '406273900@qq.com',
      license = 'MIT',
      packages = ['gameturtle'],
      zip_safe = False,
      install_requires = [ 'pillow>=2.7.0','numpy']
     )

