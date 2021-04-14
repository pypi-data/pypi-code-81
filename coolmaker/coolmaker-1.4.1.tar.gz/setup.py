from setuptools import setup,find_packages

with open("README.md", encoding='utf-8') as fh:
    long_d = fh.read()


setup(name='coolmaker',
      long_description_content_type="text/markdown",
      version = '1.4.1',
      description = '为教育目的而制作启蒙动画与游戏模块。主要提供继承自Turtle类的Sprite类。作者：酷哥创客。网址：http://www.coolguymaker.com',
      long_description = long_d,      
      keywords = 'creative game pygame turtle animation sprite',
      url = 'http://www.coolguymaker.com',
      author ='coolmaker',
      author_email = 'wangyf@coolguymaker.com',
      license = 'MIT',
      packages = ['coolmaker'],
      zip_safe = False,
      install_requires = [ 'pillow>=2.7.0','numpy']
     )

