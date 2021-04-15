from setuptools import setup

setup(
    name='Flask-Request-Logging',
    version='0.1',
    author='liuzhiyong',
    author_email='ip_hardy@qq.com',
    description='Logging for Flask Request',
    keywords = ['flask', 'logging'],
    packages=['flask_request_logging'],
    zip_safe=False,
    platforms='any',
    install_requires=['Flask']
)

