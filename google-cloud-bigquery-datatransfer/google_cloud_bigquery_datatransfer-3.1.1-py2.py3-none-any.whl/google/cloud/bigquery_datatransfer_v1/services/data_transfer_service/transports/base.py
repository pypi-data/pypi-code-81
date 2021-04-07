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

import abc
import typing
import pkg_resources

from google import auth  # type: ignore
from google.api_core import exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials  # type: ignore

from google.cloud.bigquery_datatransfer_v1.types import datatransfer
from google.cloud.bigquery_datatransfer_v1.types import transfer
from google.protobuf import empty_pb2 as empty  # type: ignore


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-bigquery-datatransfer",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


class DataTransferServiceTransport(abc.ABC):
    """Abstract transport class for DataTransferService."""

    AUTH_SCOPES = ("https://www.googleapis.com/auth/cloud-platform",)

    def __init__(
        self,
        *,
        host: str = "bigquerydatatransfer.googleapis.com",
        credentials: credentials.Credentials = None,
        credentials_file: typing.Optional[str] = None,
        scopes: typing.Optional[typing.Sequence[str]] = AUTH_SCOPES,
        quota_project_id: typing.Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        **kwargs,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]): The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is mutually exclusive with credentials.
            scope (Optional[Sequence[str]]): A list of scopes.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
        """
        # Save the hostname. Default to port 443 (HTTPS) if none is specified.
        if ":" not in host:
            host += ":443"
        self._host = host

        # Save the scopes.
        self._scopes = scopes or self.AUTH_SCOPES

        # If no credentials are provided, then determine the appropriate
        # defaults.
        if credentials and credentials_file:
            raise exceptions.DuplicateCredentialArgs(
                "'credentials_file' and 'credentials' are mutually exclusive"
            )

        if credentials_file is not None:
            credentials, _ = auth.load_credentials_from_file(
                credentials_file, scopes=self._scopes, quota_project_id=quota_project_id
            )

        elif credentials is None:
            credentials, _ = auth.default(
                scopes=self._scopes, quota_project_id=quota_project_id
            )

        # Save the credentials.
        self._credentials = credentials

    def _prep_wrapped_messages(self, client_info):
        # Precompute the wrapped methods.
        self._wrapped_methods = {
            self.get_data_source: gapic_v1.method.wrap_method(
                self.get_data_source,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                    deadline=20.0,
                ),
                default_timeout=20.0,
                client_info=client_info,
            ),
            self.list_data_sources: gapic_v1.method.wrap_method(
                self.list_data_sources,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                    deadline=20.0,
                ),
                default_timeout=20.0,
                client_info=client_info,
            ),
            self.create_transfer_config: gapic_v1.method.wrap_method(
                self.create_transfer_config,
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.update_transfer_config: gapic_v1.method.wrap_method(
                self.update_transfer_config,
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.delete_transfer_config: gapic_v1.method.wrap_method(
                self.delete_transfer_config,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                    deadline=20.0,
                ),
                default_timeout=20.0,
                client_info=client_info,
            ),
            self.get_transfer_config: gapic_v1.method.wrap_method(
                self.get_transfer_config,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                    deadline=20.0,
                ),
                default_timeout=20.0,
                client_info=client_info,
            ),
            self.list_transfer_configs: gapic_v1.method.wrap_method(
                self.list_transfer_configs,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                    deadline=20.0,
                ),
                default_timeout=20.0,
                client_info=client_info,
            ),
            self.schedule_transfer_runs: gapic_v1.method.wrap_method(
                self.schedule_transfer_runs,
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.start_manual_transfer_runs: gapic_v1.method.wrap_method(
                self.start_manual_transfer_runs,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_transfer_run: gapic_v1.method.wrap_method(
                self.get_transfer_run,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                    deadline=20.0,
                ),
                default_timeout=20.0,
                client_info=client_info,
            ),
            self.delete_transfer_run: gapic_v1.method.wrap_method(
                self.delete_transfer_run,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                    deadline=20.0,
                ),
                default_timeout=20.0,
                client_info=client_info,
            ),
            self.list_transfer_runs: gapic_v1.method.wrap_method(
                self.list_transfer_runs,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                    deadline=20.0,
                ),
                default_timeout=20.0,
                client_info=client_info,
            ),
            self.list_transfer_logs: gapic_v1.method.wrap_method(
                self.list_transfer_logs,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                    deadline=20.0,
                ),
                default_timeout=20.0,
                client_info=client_info,
            ),
            self.check_valid_creds: gapic_v1.method.wrap_method(
                self.check_valid_creds,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                    deadline=20.0,
                ),
                default_timeout=20.0,
                client_info=client_info,
            ),
        }

    @property
    def get_data_source(
        self,
    ) -> typing.Callable[
        [datatransfer.GetDataSourceRequest],
        typing.Union[
            datatransfer.DataSource, typing.Awaitable[datatransfer.DataSource]
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_data_sources(
        self,
    ) -> typing.Callable[
        [datatransfer.ListDataSourcesRequest],
        typing.Union[
            datatransfer.ListDataSourcesResponse,
            typing.Awaitable[datatransfer.ListDataSourcesResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def create_transfer_config(
        self,
    ) -> typing.Callable[
        [datatransfer.CreateTransferConfigRequest],
        typing.Union[
            transfer.TransferConfig, typing.Awaitable[transfer.TransferConfig]
        ],
    ]:
        raise NotImplementedError()

    @property
    def update_transfer_config(
        self,
    ) -> typing.Callable[
        [datatransfer.UpdateTransferConfigRequest],
        typing.Union[
            transfer.TransferConfig, typing.Awaitable[transfer.TransferConfig]
        ],
    ]:
        raise NotImplementedError()

    @property
    def delete_transfer_config(
        self,
    ) -> typing.Callable[
        [datatransfer.DeleteTransferConfigRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def get_transfer_config(
        self,
    ) -> typing.Callable[
        [datatransfer.GetTransferConfigRequest],
        typing.Union[
            transfer.TransferConfig, typing.Awaitable[transfer.TransferConfig]
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_transfer_configs(
        self,
    ) -> typing.Callable[
        [datatransfer.ListTransferConfigsRequest],
        typing.Union[
            datatransfer.ListTransferConfigsResponse,
            typing.Awaitable[datatransfer.ListTransferConfigsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def schedule_transfer_runs(
        self,
    ) -> typing.Callable[
        [datatransfer.ScheduleTransferRunsRequest],
        typing.Union[
            datatransfer.ScheduleTransferRunsResponse,
            typing.Awaitable[datatransfer.ScheduleTransferRunsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def start_manual_transfer_runs(
        self,
    ) -> typing.Callable[
        [datatransfer.StartManualTransferRunsRequest],
        typing.Union[
            datatransfer.StartManualTransferRunsResponse,
            typing.Awaitable[datatransfer.StartManualTransferRunsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_transfer_run(
        self,
    ) -> typing.Callable[
        [datatransfer.GetTransferRunRequest],
        typing.Union[transfer.TransferRun, typing.Awaitable[transfer.TransferRun]],
    ]:
        raise NotImplementedError()

    @property
    def delete_transfer_run(
        self,
    ) -> typing.Callable[
        [datatransfer.DeleteTransferRunRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def list_transfer_runs(
        self,
    ) -> typing.Callable[
        [datatransfer.ListTransferRunsRequest],
        typing.Union[
            datatransfer.ListTransferRunsResponse,
            typing.Awaitable[datatransfer.ListTransferRunsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_transfer_logs(
        self,
    ) -> typing.Callable[
        [datatransfer.ListTransferLogsRequest],
        typing.Union[
            datatransfer.ListTransferLogsResponse,
            typing.Awaitable[datatransfer.ListTransferLogsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def check_valid_creds(
        self,
    ) -> typing.Callable[
        [datatransfer.CheckValidCredsRequest],
        typing.Union[
            datatransfer.CheckValidCredsResponse,
            typing.Awaitable[datatransfer.CheckValidCredsResponse],
        ],
    ]:
        raise NotImplementedError()


__all__ = ("DataTransferServiceTransport",)
