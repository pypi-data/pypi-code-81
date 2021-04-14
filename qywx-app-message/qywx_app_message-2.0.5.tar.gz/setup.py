from setuptools import setup, find_packages

setup(
      name='qywx_app_message',
      version='2.0.5',
      description = "企业微信应用推送消息",
      long_description = "https://github.com/not-know/qywx_app_message",
      url='https://github.com/not-know/qywx_app_message',
      author='zhr',
      author_email='zhangran1033@gmail.com',
      license='MIT Licence',
      
      packages = find_packages(),
      include_package_data = True,
      platforms = "any",
      install_requires = ["requests"]
      )