from setuptools import setup

setup(name = 'rmk-distributions',
version = '0.2',
author = 'Ryan Keeler',
author_email = 'keeler.rm@gmail.com',
description = 'Derive binomial and normal distributions from a given set of values',
packages = ['rmk-distributions'], # If I have multiple packages in this root folder, I tell python/pip to find them witht this.
zip_safe = False)
