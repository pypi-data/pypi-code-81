# -*- coding: utf-8 -*-

# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import proto  # type: ignore


__protobuf__ = proto.module(
    package="google.appengine.v1", manifest={"LocationMetadata",},
)


class LocationMetadata(proto.Message):
    r"""Metadata for the given
    [google.cloud.location.Location][google.cloud.location.Location].

    Attributes:
        standard_environment_available (bool):
            App Engine standard environment is available
            in the given location.
            @OutputOnly
        flexible_environment_available (bool):
            App Engine flexible environment is available
            in the given location.
            @OutputOnly
        search_api_available (bool):
            Output only. `Search
            API <https://cloud.google.com/appengine/docs/standard/python/search>`__
            is available in the given location.
    """

    standard_environment_available = proto.Field(proto.BOOL, number=2)

    flexible_environment_available = proto.Field(proto.BOOL, number=4)

    search_api_available = proto.Field(proto.BOOL, number=6)


__all__ = tuple(sorted(__protobuf__.manifest))
