#  actorname: library for generating human-readable, random names
#           for objects (e.g. hostnames, containers, blobs)
#
#  Copyright 2021 Mark Christopher West <markchristopherwest@gmail.com>
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.


import random
import re
from .english import names


try:
	random = random.SystemRandom()
except NotImplementedError:
	pass # less secure


def name(letters=12):
	while 1:
		w = random.choice(names)
		if len(w) <= letters:
			return w


def generate(words=2, separator="-", letters=12):
	target = name(letters)
	if words == 1:
		return target[0]
	elif words == 2:
		return re.split('\s+', target)[0] + separator + re.split('\s+', target)[1]
	return separator.join(re.split('\s+', target))
	

# aliases for backwards compatiblity
Name = name
Generate = generate
