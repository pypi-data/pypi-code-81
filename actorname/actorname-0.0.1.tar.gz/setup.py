#!/usr/bin/env python3
#
# actorname - library for generating human-readable, random names
#           for objects (e.g. hostnames, containers, blobs)
# Copyright (c) 2013 Casey Marshall <casey.marshall@gmail.com>
# Copyright (c) 2019 Mark Christopher West <markchristopherwest@gmail.com>
#
# ssh-import-id is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# ssh-import-id is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with python-actorname.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup

with open("README.md", "r") as fh:
	long_description = fh.read()

setup(
	name='actorname',
	description='Generate human-readable, random object names',
	#long_description=long_description,
	#long_description_content_type="text/markdown",
	version='0.0.1',
	author='Mark Christopher West',
	author_email='markchristopherwest@gmail.com',
	license="Apache2",
	keywords="random name uuid",
	url='https://launchpad.net/python-actorname',
	platforms=['any'],
	packages=['actorname'],
	entry_points={
		'console_scripts': [
			'actorname = actorname.__main__:main',
		]
	},
)
