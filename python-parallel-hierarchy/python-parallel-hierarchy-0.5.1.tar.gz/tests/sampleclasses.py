#
#     Copyright 2021 Joël Larose
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.
#
#

from dataclasses import dataclass, field

@dataclass
class A:
    z: int = 0
    y: float = 0.0

@dataclass
class B(A):
    x: str = ""

@dataclass
class C(A):
    w: list = field(default_factory=list)

class Mixin:
    pass

@dataclass
class D(Mixin, C):
    v: set = field(default_factory=set)

@dataclass
class E(B, D):
    pass

class View:
    pass
