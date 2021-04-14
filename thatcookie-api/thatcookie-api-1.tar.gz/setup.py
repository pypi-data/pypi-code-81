from distutils.core import setup
setup(
  name = "thatcookie-api",
  packages = ["thatcookieapi"],
  version = 1,
  license = 'GNU General Public License v3 or later (GPLv3+)',
  description = "Something to make interacting with Cookie's API easy",
  author = "ThatCookie",
  author_email = "contact.thatcookie@gmail.com",
  url = "https://github.com/ThatCookie",
  download_url = "https://github.com/ThatCookie/cookieapi-python-wrapper/archive/refs/tags/1.tar.gz",
  keywords = ['API', 'Cookie', 'ThatCookie'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
    'requests',
  ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ], 
)