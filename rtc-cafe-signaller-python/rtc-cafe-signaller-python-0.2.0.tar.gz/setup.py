try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='rtc-cafe-signaller-python',
    version='v0.2.0',
    url='https://gitlab.com/rtc-cafe/rtc-cafe-signaller-python',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=[
        'rtc_cafe_signaller',
        'rtc_cafe_signaller.wrappers',
    ],
)
