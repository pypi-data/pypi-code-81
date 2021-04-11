# python setup.py sdist
# python setup.py bdist_wheel
# twine upload dist/*0.2.0*

import setuptools
import io
import os

setuptools.setup(
    name='grid2demand',
    version='0.2.0',
    author='Anjun Li, Xuesong (Simon) Zhou, Entai Wang, Taehooie Kim',
    author_email='anjun.li93@gmail.com, xzhou74@asu.edu, entaiwang@bjtu.edu.cn, taehooie.kim@asu.edu',
    url='https://github.com/asu-trans-ai-lab/grid2demand',
    description='A tool for generating zone-to-zone travel demand based on grid cells',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    license='GPLv3+',
    packages=['grid2demand'],
    python_requires=">=3.6.0",
    install_requires=['pandas >= 0.24.0', 'numpy'],
    classifiers=['License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
                 'Programming Language :: Python :: 3']
)
