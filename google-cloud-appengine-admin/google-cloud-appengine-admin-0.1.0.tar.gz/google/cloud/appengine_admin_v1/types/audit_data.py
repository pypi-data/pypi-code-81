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


from google.cloud.appengine_admin_v1.types import appengine


__protobuf__ = proto.module(
    package="google.appengine.v1",
    manifest={"AuditData", "UpdateServiceMethod", "CreateVersionMethod",},
)


class AuditData(proto.Message):
    r"""App Engine admin service audit log.

    Attributes:
        update_service (google.cloud.appengine_admin_v1.types.UpdateServiceMethod):
            Detailed information about UpdateService
            call.
        create_version (google.cloud.appengine_admin_v1.types.CreateVersionMethod):
            Detailed information about CreateVersion
            call.
    """

    update_service = proto.Field(
        proto.MESSAGE, number=1, oneof="method", message="UpdateServiceMethod",
    )

    create_version = proto.Field(
        proto.MESSAGE, number=2, oneof="method", message="CreateVersionMethod",
    )


class UpdateServiceMethod(proto.Message):
    r"""Detailed information about UpdateService call.

    Attributes:
        request (google.cloud.appengine_admin_v1.types.UpdateServiceRequest):
            Update service request.
    """

    request = proto.Field(
        proto.MESSAGE, number=1, message=appengine.UpdateServiceRequest,
    )


class CreateVersionMethod(proto.Message):
    r"""Detailed information about CreateVersion call.

    Attributes:
        request (google.cloud.appengine_admin_v1.types.CreateVersionRequest):
            Create version request.
    """

    request = proto.Field(
        proto.MESSAGE, number=1, message=appengine.CreateVersionRequest,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
