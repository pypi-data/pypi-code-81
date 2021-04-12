from setuptools import setup, find_packages
import buildtools

install_requires = [
    "requests>=1.0",
    "ConfigArgParse>=1.0",
    "argcomplete>=1.0",
    "anytree>=2.0",
    "art>=2.0",
    "mistletoe-tcopy>=0.7.2",
]

setup(name="ntsbuildtools",
      packages=find_packages(),
      version=buildtools.__version__,
      license='MIT',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
      description="CLI tools that support NTS Jenkins pipelines.",
      author='University of Oregon',
      author_email='rleonar7@uoregon.edu',
      url='https://git.uoregon.edu/projects/ISN/repos/jenkins_py_scripts/browse',
      keywords=['Jenkins', 'NTS', 'UO', 'CLI', 'Integrations', 'API'],  # Keywords that define your package best
      scripts=['bin/buildtools'],
      install_requires=install_requires,
      setup_requires=install_requires,
      classifiers=[
          'Development Status :: 3 - Alpha',
          # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
          'Intended Audience :: Developers',  # Define that your audience are developers
          'Topic :: Software Development :: Build Tools',
          'License :: OSI Approved :: MIT License',  # Again, pick a license
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
      ]
      )
