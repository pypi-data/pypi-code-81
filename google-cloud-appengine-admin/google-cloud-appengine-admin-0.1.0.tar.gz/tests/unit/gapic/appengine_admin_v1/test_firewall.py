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

import os
import mock

import grpc
from grpc.experimental import aio
import math
import pytest
from proto.marshal.rules.dates import DurationRule, TimestampRule

from google import auth
from google.api_core import client_options
from google.api_core import exceptions
from google.api_core import gapic_v1
from google.api_core import grpc_helpers
from google.api_core import grpc_helpers_async
from google.auth import credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.appengine_admin_v1.services.firewall import FirewallAsyncClient
from google.cloud.appengine_admin_v1.services.firewall import FirewallClient
from google.cloud.appengine_admin_v1.services.firewall import pagers
from google.cloud.appengine_admin_v1.services.firewall import transports
from google.cloud.appengine_admin_v1.types import appengine
from google.cloud.appengine_admin_v1.types import firewall
from google.oauth2 import service_account
from google.protobuf import field_mask_pb2 as field_mask  # type: ignore


def client_cert_source_callback():
    return b"cert bytes", b"key bytes"


# If default endpoint is localhost, then default mtls endpoint will be the same.
# This method modifies the default endpoint so the client can produce a different
# mtls endpoint for endpoint testing purposes.
def modify_default_endpoint(client):
    return (
        "foo.googleapis.com"
        if ("localhost" in client.DEFAULT_ENDPOINT)
        else client.DEFAULT_ENDPOINT
    )


def test__get_default_mtls_endpoint():
    api_endpoint = "example.googleapis.com"
    api_mtls_endpoint = "example.mtls.googleapis.com"
    sandbox_endpoint = "example.sandbox.googleapis.com"
    sandbox_mtls_endpoint = "example.mtls.sandbox.googleapis.com"
    non_googleapi = "api.example.com"

    assert FirewallClient._get_default_mtls_endpoint(None) is None
    assert FirewallClient._get_default_mtls_endpoint(api_endpoint) == api_mtls_endpoint
    assert (
        FirewallClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        FirewallClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        FirewallClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert FirewallClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi


@pytest.mark.parametrize("client_class", [FirewallClient, FirewallAsyncClient,])
def test_firewall_client_from_service_account_info(client_class):
    creds = credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == "appengine.googleapis.com:443"


@pytest.mark.parametrize("client_class", [FirewallClient, FirewallAsyncClient,])
def test_firewall_client_from_service_account_file(client_class):
    creds = credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file("dummy/file/path.json")
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        client = client_class.from_service_account_json("dummy/file/path.json")
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == "appengine.googleapis.com:443"


def test_firewall_client_get_transport_class():
    transport = FirewallClient.get_transport_class()
    available_transports = [
        transports.FirewallGrpcTransport,
    ]
    assert transport in available_transports

    transport = FirewallClient.get_transport_class("grpc")
    assert transport == transports.FirewallGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (FirewallClient, transports.FirewallGrpcTransport, "grpc"),
        (FirewallAsyncClient, transports.FirewallGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
@mock.patch.object(
    FirewallClient, "DEFAULT_ENDPOINT", modify_default_endpoint(FirewallClient)
)
@mock.patch.object(
    FirewallAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(FirewallAsyncClient),
)
def test_firewall_client_client_options(client_class, transport_class, transport_name):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(FirewallClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(FirewallClient, "get_transport_class") as gtc:
        client = client_class(transport=transport_name)
        gtc.assert_called()

    # Check the case api_endpoint is provided.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class()
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class()
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError):
            client = client_class()

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError):
            client = client_class()

    # Check the case quota_project_id is provided
    options = client_options.ClientOptions(quota_project_id="octopus")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id="octopus",
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,use_client_cert_env",
    [
        (FirewallClient, transports.FirewallGrpcTransport, "grpc", "true"),
        (
            FirewallAsyncClient,
            transports.FirewallGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (FirewallClient, transports.FirewallGrpcTransport, "grpc", "false"),
        (
            FirewallAsyncClient,
            transports.FirewallGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    FirewallClient, "DEFAULT_ENDPOINT", modify_default_endpoint(FirewallClient)
)
@mock.patch.object(
    FirewallAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(FirewallAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_firewall_client_mtls_env_auto(
    client_class, transport_class, transport_name, use_client_cert_env
):
    # This tests the endpoint autoswitch behavior. Endpoint is autoswitched to the default
    # mtls endpoint, if GOOGLE_API_USE_CLIENT_CERTIFICATE is "true" and client cert exists.

    # Check the case client_cert_source is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        options = client_options.ClientOptions(
            client_cert_source=client_cert_source_callback
        )
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options)

            if use_client_cert_env == "false":
                expected_client_cert_source = None
                expected_host = client.DEFAULT_ENDPOINT
            else:
                expected_client_cert_source = client_cert_source_callback
                expected_host = client.DEFAULT_MTLS_ENDPOINT

            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=expected_host,
                scopes=None,
                client_cert_source_for_mtls=expected_client_cert_source,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
            )

    # Check the case ADC client cert is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=True,
            ):
                with mock.patch(
                    "google.auth.transport.mtls.default_client_cert_source",
                    return_value=client_cert_source_callback,
                ):
                    if use_client_cert_env == "false":
                        expected_host = client.DEFAULT_ENDPOINT
                        expected_client_cert_source = None
                    else:
                        expected_host = client.DEFAULT_MTLS_ENDPOINT
                        expected_client_cert_source = client_cert_source_callback

                    patched.return_value = None
                    client = client_class()
                    patched.assert_called_once_with(
                        credentials=None,
                        credentials_file=None,
                        host=expected_host,
                        scopes=None,
                        client_cert_source_for_mtls=expected_client_cert_source,
                        quota_project_id=None,
                        client_info=transports.base.DEFAULT_CLIENT_INFO,
                    )

    # Check the case client_cert_source and ADC client cert are not provided.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=False,
            ):
                patched.return_value = None
                client = client_class()
                patched.assert_called_once_with(
                    credentials=None,
                    credentials_file=None,
                    host=client.DEFAULT_ENDPOINT,
                    scopes=None,
                    client_cert_source_for_mtls=None,
                    quota_project_id=None,
                    client_info=transports.base.DEFAULT_CLIENT_INFO,
                )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (FirewallClient, transports.FirewallGrpcTransport, "grpc"),
        (FirewallAsyncClient, transports.FirewallGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
def test_firewall_client_client_options_scopes(
    client_class, transport_class, transport_name
):
    # Check the case scopes are provided.
    options = client_options.ClientOptions(scopes=["1", "2"],)
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=["1", "2"],
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (FirewallClient, transports.FirewallGrpcTransport, "grpc"),
        (FirewallAsyncClient, transports.FirewallGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
def test_firewall_client_client_options_credentials_file(
    client_class, transport_class, transport_name
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


def test_firewall_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.appengine_admin_v1.services.firewall.transports.FirewallGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = FirewallClient(client_options={"api_endpoint": "squid.clam.whelk"})
        grpc_transport.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


def test_list_ingress_rules(
    transport: str = "grpc", request_type=appengine.ListIngressRulesRequest
):
    client = FirewallClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_ingress_rules), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = appengine.ListIngressRulesResponse(
            next_page_token="next_page_token_value",
        )

        response = client.list_ingress_rules(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == appengine.ListIngressRulesRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, pagers.ListIngressRulesPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_ingress_rules_from_dict():
    test_list_ingress_rules(request_type=dict)


def test_list_ingress_rules_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = FirewallClient(
        credentials=credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_ingress_rules), "__call__"
    ) as call:
        client.list_ingress_rules()
        call.assert_called()
        _, args, _ = call.mock_calls[0]

        assert args[0] == appengine.ListIngressRulesRequest()


@pytest.mark.asyncio
async def test_list_ingress_rules_async(
    transport: str = "grpc_asyncio", request_type=appengine.ListIngressRulesRequest
):
    client = FirewallAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_ingress_rules), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            appengine.ListIngressRulesResponse(next_page_token="next_page_token_value",)
        )

        response = await client.list_ingress_rules(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == appengine.ListIngressRulesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListIngressRulesAsyncPager)

    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_ingress_rules_async_from_dict():
    await test_list_ingress_rules_async(request_type=dict)


def test_list_ingress_rules_field_headers():
    client = FirewallClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = appengine.ListIngressRulesRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_ingress_rules), "__call__"
    ) as call:
        call.return_value = appengine.ListIngressRulesResponse()

        client.list_ingress_rules(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_ingress_rules_field_headers_async():
    client = FirewallAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = appengine.ListIngressRulesRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_ingress_rules), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            appengine.ListIngressRulesResponse()
        )

        await client.list_ingress_rules(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_ingress_rules_pager():
    client = FirewallClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_ingress_rules), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            appengine.ListIngressRulesResponse(
                ingress_rules=[
                    firewall.FirewallRule(),
                    firewall.FirewallRule(),
                    firewall.FirewallRule(),
                ],
                next_page_token="abc",
            ),
            appengine.ListIngressRulesResponse(
                ingress_rules=[], next_page_token="def",
            ),
            appengine.ListIngressRulesResponse(
                ingress_rules=[firewall.FirewallRule(),], next_page_token="ghi",
            ),
            appengine.ListIngressRulesResponse(
                ingress_rules=[firewall.FirewallRule(), firewall.FirewallRule(),],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_ingress_rules(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, firewall.FirewallRule) for i in results)


def test_list_ingress_rules_pages():
    client = FirewallClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_ingress_rules), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            appengine.ListIngressRulesResponse(
                ingress_rules=[
                    firewall.FirewallRule(),
                    firewall.FirewallRule(),
                    firewall.FirewallRule(),
                ],
                next_page_token="abc",
            ),
            appengine.ListIngressRulesResponse(
                ingress_rules=[], next_page_token="def",
            ),
            appengine.ListIngressRulesResponse(
                ingress_rules=[firewall.FirewallRule(),], next_page_token="ghi",
            ),
            appengine.ListIngressRulesResponse(
                ingress_rules=[firewall.FirewallRule(), firewall.FirewallRule(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_ingress_rules(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_ingress_rules_async_pager():
    client = FirewallAsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_ingress_rules),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            appengine.ListIngressRulesResponse(
                ingress_rules=[
                    firewall.FirewallRule(),
                    firewall.FirewallRule(),
                    firewall.FirewallRule(),
                ],
                next_page_token="abc",
            ),
            appengine.ListIngressRulesResponse(
                ingress_rules=[], next_page_token="def",
            ),
            appengine.ListIngressRulesResponse(
                ingress_rules=[firewall.FirewallRule(),], next_page_token="ghi",
            ),
            appengine.ListIngressRulesResponse(
                ingress_rules=[firewall.FirewallRule(), firewall.FirewallRule(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_ingress_rules(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, firewall.FirewallRule) for i in responses)


@pytest.mark.asyncio
async def test_list_ingress_rules_async_pages():
    client = FirewallAsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_ingress_rules),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            appengine.ListIngressRulesResponse(
                ingress_rules=[
                    firewall.FirewallRule(),
                    firewall.FirewallRule(),
                    firewall.FirewallRule(),
                ],
                next_page_token="abc",
            ),
            appengine.ListIngressRulesResponse(
                ingress_rules=[], next_page_token="def",
            ),
            appengine.ListIngressRulesResponse(
                ingress_rules=[firewall.FirewallRule(),], next_page_token="ghi",
            ),
            appengine.ListIngressRulesResponse(
                ingress_rules=[firewall.FirewallRule(), firewall.FirewallRule(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_ingress_rules(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_batch_update_ingress_rules(
    transport: str = "grpc", request_type=appengine.BatchUpdateIngressRulesRequest
):
    client = FirewallClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_update_ingress_rules), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = appengine.BatchUpdateIngressRulesResponse()

        response = client.batch_update_ingress_rules(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == appengine.BatchUpdateIngressRulesRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, appengine.BatchUpdateIngressRulesResponse)


def test_batch_update_ingress_rules_from_dict():
    test_batch_update_ingress_rules(request_type=dict)


def test_batch_update_ingress_rules_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = FirewallClient(
        credentials=credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_update_ingress_rules), "__call__"
    ) as call:
        client.batch_update_ingress_rules()
        call.assert_called()
        _, args, _ = call.mock_calls[0]

        assert args[0] == appengine.BatchUpdateIngressRulesRequest()


@pytest.mark.asyncio
async def test_batch_update_ingress_rules_async(
    transport: str = "grpc_asyncio",
    request_type=appengine.BatchUpdateIngressRulesRequest,
):
    client = FirewallAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_update_ingress_rules), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            appengine.BatchUpdateIngressRulesResponse()
        )

        response = await client.batch_update_ingress_rules(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == appengine.BatchUpdateIngressRulesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, appengine.BatchUpdateIngressRulesResponse)


@pytest.mark.asyncio
async def test_batch_update_ingress_rules_async_from_dict():
    await test_batch_update_ingress_rules_async(request_type=dict)


def test_batch_update_ingress_rules_field_headers():
    client = FirewallClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = appengine.BatchUpdateIngressRulesRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_update_ingress_rules), "__call__"
    ) as call:
        call.return_value = appengine.BatchUpdateIngressRulesResponse()

        client.batch_update_ingress_rules(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_batch_update_ingress_rules_field_headers_async():
    client = FirewallAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = appengine.BatchUpdateIngressRulesRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_update_ingress_rules), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            appengine.BatchUpdateIngressRulesResponse()
        )

        await client.batch_update_ingress_rules(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_create_ingress_rule(
    transport: str = "grpc", request_type=appengine.CreateIngressRuleRequest
):
    client = FirewallClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_ingress_rule), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = firewall.FirewallRule(
            priority=898,
            action=firewall.FirewallRule.Action.ALLOW,
            source_range="source_range_value",
            description="description_value",
        )

        response = client.create_ingress_rule(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == appengine.CreateIngressRuleRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, firewall.FirewallRule)

    assert response.priority == 898

    assert response.action == firewall.FirewallRule.Action.ALLOW

    assert response.source_range == "source_range_value"

    assert response.description == "description_value"


def test_create_ingress_rule_from_dict():
    test_create_ingress_rule(request_type=dict)


def test_create_ingress_rule_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = FirewallClient(
        credentials=credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_ingress_rule), "__call__"
    ) as call:
        client.create_ingress_rule()
        call.assert_called()
        _, args, _ = call.mock_calls[0]

        assert args[0] == appengine.CreateIngressRuleRequest()


@pytest.mark.asyncio
async def test_create_ingress_rule_async(
    transport: str = "grpc_asyncio", request_type=appengine.CreateIngressRuleRequest
):
    client = FirewallAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_ingress_rule), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            firewall.FirewallRule(
                priority=898,
                action=firewall.FirewallRule.Action.ALLOW,
                source_range="source_range_value",
                description="description_value",
            )
        )

        response = await client.create_ingress_rule(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == appengine.CreateIngressRuleRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, firewall.FirewallRule)

    assert response.priority == 898

    assert response.action == firewall.FirewallRule.Action.ALLOW

    assert response.source_range == "source_range_value"

    assert response.description == "description_value"


@pytest.mark.asyncio
async def test_create_ingress_rule_async_from_dict():
    await test_create_ingress_rule_async(request_type=dict)


def test_create_ingress_rule_field_headers():
    client = FirewallClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = appengine.CreateIngressRuleRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_ingress_rule), "__call__"
    ) as call:
        call.return_value = firewall.FirewallRule()

        client.create_ingress_rule(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_ingress_rule_field_headers_async():
    client = FirewallAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = appengine.CreateIngressRuleRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_ingress_rule), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            firewall.FirewallRule()
        )

        await client.create_ingress_rule(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_get_ingress_rule(
    transport: str = "grpc", request_type=appengine.GetIngressRuleRequest
):
    client = FirewallClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_ingress_rule), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = firewall.FirewallRule(
            priority=898,
            action=firewall.FirewallRule.Action.ALLOW,
            source_range="source_range_value",
            description="description_value",
        )

        response = client.get_ingress_rule(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == appengine.GetIngressRuleRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, firewall.FirewallRule)

    assert response.priority == 898

    assert response.action == firewall.FirewallRule.Action.ALLOW

    assert response.source_range == "source_range_value"

    assert response.description == "description_value"


def test_get_ingress_rule_from_dict():
    test_get_ingress_rule(request_type=dict)


def test_get_ingress_rule_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = FirewallClient(
        credentials=credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_ingress_rule), "__call__") as call:
        client.get_ingress_rule()
        call.assert_called()
        _, args, _ = call.mock_calls[0]

        assert args[0] == appengine.GetIngressRuleRequest()


@pytest.mark.asyncio
async def test_get_ingress_rule_async(
    transport: str = "grpc_asyncio", request_type=appengine.GetIngressRuleRequest
):
    client = FirewallAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_ingress_rule), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            firewall.FirewallRule(
                priority=898,
                action=firewall.FirewallRule.Action.ALLOW,
                source_range="source_range_value",
                description="description_value",
            )
        )

        response = await client.get_ingress_rule(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == appengine.GetIngressRuleRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, firewall.FirewallRule)

    assert response.priority == 898

    assert response.action == firewall.FirewallRule.Action.ALLOW

    assert response.source_range == "source_range_value"

    assert response.description == "description_value"


@pytest.mark.asyncio
async def test_get_ingress_rule_async_from_dict():
    await test_get_ingress_rule_async(request_type=dict)


def test_get_ingress_rule_field_headers():
    client = FirewallClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = appengine.GetIngressRuleRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_ingress_rule), "__call__") as call:
        call.return_value = firewall.FirewallRule()

        client.get_ingress_rule(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_ingress_rule_field_headers_async():
    client = FirewallAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = appengine.GetIngressRuleRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_ingress_rule), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            firewall.FirewallRule()
        )

        await client.get_ingress_rule(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_update_ingress_rule(
    transport: str = "grpc", request_type=appengine.UpdateIngressRuleRequest
):
    client = FirewallClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_ingress_rule), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = firewall.FirewallRule(
            priority=898,
            action=firewall.FirewallRule.Action.ALLOW,
            source_range="source_range_value",
            description="description_value",
        )

        response = client.update_ingress_rule(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == appengine.UpdateIngressRuleRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, firewall.FirewallRule)

    assert response.priority == 898

    assert response.action == firewall.FirewallRule.Action.ALLOW

    assert response.source_range == "source_range_value"

    assert response.description == "description_value"


def test_update_ingress_rule_from_dict():
    test_update_ingress_rule(request_type=dict)


def test_update_ingress_rule_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = FirewallClient(
        credentials=credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_ingress_rule), "__call__"
    ) as call:
        client.update_ingress_rule()
        call.assert_called()
        _, args, _ = call.mock_calls[0]

        assert args[0] == appengine.UpdateIngressRuleRequest()


@pytest.mark.asyncio
async def test_update_ingress_rule_async(
    transport: str = "grpc_asyncio", request_type=appengine.UpdateIngressRuleRequest
):
    client = FirewallAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_ingress_rule), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            firewall.FirewallRule(
                priority=898,
                action=firewall.FirewallRule.Action.ALLOW,
                source_range="source_range_value",
                description="description_value",
            )
        )

        response = await client.update_ingress_rule(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == appengine.UpdateIngressRuleRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, firewall.FirewallRule)

    assert response.priority == 898

    assert response.action == firewall.FirewallRule.Action.ALLOW

    assert response.source_range == "source_range_value"

    assert response.description == "description_value"


@pytest.mark.asyncio
async def test_update_ingress_rule_async_from_dict():
    await test_update_ingress_rule_async(request_type=dict)


def test_update_ingress_rule_field_headers():
    client = FirewallClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = appengine.UpdateIngressRuleRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_ingress_rule), "__call__"
    ) as call:
        call.return_value = firewall.FirewallRule()

        client.update_ingress_rule(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_ingress_rule_field_headers_async():
    client = FirewallAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = appengine.UpdateIngressRuleRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_ingress_rule), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            firewall.FirewallRule()
        )

        await client.update_ingress_rule(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_ingress_rule(
    transport: str = "grpc", request_type=appengine.DeleteIngressRuleRequest
):
    client = FirewallClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_ingress_rule), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.delete_ingress_rule(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == appengine.DeleteIngressRuleRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_ingress_rule_from_dict():
    test_delete_ingress_rule(request_type=dict)


def test_delete_ingress_rule_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = FirewallClient(
        credentials=credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_ingress_rule), "__call__"
    ) as call:
        client.delete_ingress_rule()
        call.assert_called()
        _, args, _ = call.mock_calls[0]

        assert args[0] == appengine.DeleteIngressRuleRequest()


@pytest.mark.asyncio
async def test_delete_ingress_rule_async(
    transport: str = "grpc_asyncio", request_type=appengine.DeleteIngressRuleRequest
):
    client = FirewallAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_ingress_rule), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        response = await client.delete_ingress_rule(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == appengine.DeleteIngressRuleRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_ingress_rule_async_from_dict():
    await test_delete_ingress_rule_async(request_type=dict)


def test_delete_ingress_rule_field_headers():
    client = FirewallClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = appengine.DeleteIngressRuleRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_ingress_rule), "__call__"
    ) as call:
        call.return_value = None

        client.delete_ingress_rule(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_ingress_rule_field_headers_async():
    client = FirewallAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = appengine.DeleteIngressRuleRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_ingress_rule), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        await client.delete_ingress_rule(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.FirewallGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = FirewallClient(
            credentials=credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.FirewallGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = FirewallClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.FirewallGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = FirewallClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.FirewallGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    client = FirewallClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.FirewallGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.FirewallGrpcAsyncIOTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [transports.FirewallGrpcTransport, transports.FirewallGrpcAsyncIOTransport,],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = FirewallClient(credentials=credentials.AnonymousCredentials(),)
    assert isinstance(client.transport, transports.FirewallGrpcTransport,)


def test_firewall_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(exceptions.DuplicateCredentialArgs):
        transport = transports.FirewallTransport(
            credentials=credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_firewall_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.appengine_admin_v1.services.firewall.transports.FirewallTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.FirewallTransport(
            credentials=credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "list_ingress_rules",
        "batch_update_ingress_rules",
        "create_ingress_rule",
        "get_ingress_rule",
        "update_ingress_rule",
        "delete_ingress_rule",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())


def test_firewall_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        auth, "load_credentials_from_file"
    ) as load_creds, mock.patch(
        "google.cloud.appengine_admin_v1.services.firewall.transports.FirewallTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (credentials.AnonymousCredentials(), None)
        transport = transports.FirewallTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=(
                "https://www.googleapis.com/auth/appengine.admin",
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/cloud-platform.read-only",
            ),
            quota_project_id="octopus",
        )


def test_firewall_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(auth, "default") as adc, mock.patch(
        "google.cloud.appengine_admin_v1.services.firewall.transports.FirewallTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transport = transports.FirewallTransport()
        adc.assert_called_once()


def test_firewall_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        FirewallClient()
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/appengine.admin",
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/cloud-platform.read-only",
            ),
            quota_project_id=None,
        )


def test_firewall_transport_auth_adc():
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transports.FirewallGrpcTransport(
            host="squid.clam.whelk", quota_project_id="octopus"
        )
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/appengine.admin",
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/cloud-platform.read-only",
            ),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class",
    [transports.FirewallGrpcTransport, transports.FirewallGrpcAsyncIOTransport],
)
def test_firewall_grpc_transport_client_cert_source_for_mtls(transport_class):
    cred = credentials.AnonymousCredentials()

    # Check ssl_channel_credentials is used if provided.
    with mock.patch.object(transport_class, "create_channel") as mock_create_channel:
        mock_ssl_channel_creds = mock.Mock()
        transport_class(
            host="squid.clam.whelk",
            credentials=cred,
            ssl_channel_credentials=mock_ssl_channel_creds,
        )
        mock_create_channel.assert_called_once_with(
            "squid.clam.whelk:443",
            credentials=cred,
            credentials_file=None,
            scopes=(
                "https://www.googleapis.com/auth/appengine.admin",
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/cloud-platform.read-only",
            ),
            ssl_credentials=mock_ssl_channel_creds,
            quota_project_id=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )

    # Check if ssl_channel_credentials is not provided, then client_cert_source_for_mtls
    # is used.
    with mock.patch.object(transport_class, "create_channel", return_value=mock.Mock()):
        with mock.patch("grpc.ssl_channel_credentials") as mock_ssl_cred:
            transport_class(
                credentials=cred,
                client_cert_source_for_mtls=client_cert_source_callback,
            )
            expected_cert, expected_key = client_cert_source_callback()
            mock_ssl_cred.assert_called_once_with(
                certificate_chain=expected_cert, private_key=expected_key
            )


def test_firewall_host_no_port():
    client = FirewallClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="appengine.googleapis.com"
        ),
    )
    assert client.transport._host == "appengine.googleapis.com:443"


def test_firewall_host_with_port():
    client = FirewallClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="appengine.googleapis.com:8000"
        ),
    )
    assert client.transport._host == "appengine.googleapis.com:8000"


def test_firewall_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.FirewallGrpcTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_firewall_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.FirewallGrpcAsyncIOTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize(
    "transport_class",
    [transports.FirewallGrpcTransport, transports.FirewallGrpcAsyncIOTransport],
)
def test_firewall_transport_channel_mtls_with_client_cert_source(transport_class):
    with mock.patch(
        "grpc.ssl_channel_credentials", autospec=True
    ) as grpc_ssl_channel_cred:
        with mock.patch.object(
            transport_class, "create_channel"
        ) as grpc_create_channel:
            mock_ssl_cred = mock.Mock()
            grpc_ssl_channel_cred.return_value = mock_ssl_cred

            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel

            cred = credentials.AnonymousCredentials()
            with pytest.warns(DeprecationWarning):
                with mock.patch.object(auth, "default") as adc:
                    adc.return_value = (cred, None)
                    transport = transport_class(
                        host="squid.clam.whelk",
                        api_mtls_endpoint="mtls.squid.clam.whelk",
                        client_cert_source=client_cert_source_callback,
                    )
                    adc.assert_called_once()

            grpc_ssl_channel_cred.assert_called_once_with(
                certificate_chain=b"cert bytes", private_key=b"key bytes"
            )
            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=cred,
                credentials_file=None,
                scopes=(
                    "https://www.googleapis.com/auth/appengine.admin",
                    "https://www.googleapis.com/auth/cloud-platform",
                    "https://www.googleapis.com/auth/cloud-platform.read-only",
                ),
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel
            assert transport._ssl_channel_credentials == mock_ssl_cred


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize(
    "transport_class",
    [transports.FirewallGrpcTransport, transports.FirewallGrpcAsyncIOTransport],
)
def test_firewall_transport_channel_mtls_with_adc(transport_class):
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        with mock.patch.object(
            transport_class, "create_channel"
        ) as grpc_create_channel:
            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel
            mock_cred = mock.Mock()

            with pytest.warns(DeprecationWarning):
                transport = transport_class(
                    host="squid.clam.whelk",
                    credentials=mock_cred,
                    api_mtls_endpoint="mtls.squid.clam.whelk",
                    client_cert_source=None,
                )

            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=mock_cred,
                credentials_file=None,
                scopes=(
                    "https://www.googleapis.com/auth/appengine.admin",
                    "https://www.googleapis.com/auth/cloud-platform",
                    "https://www.googleapis.com/auth/cloud-platform.read-only",
                ),
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel


def test_common_billing_account_path():
    billing_account = "squid"

    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = FirewallClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "clam",
    }
    path = FirewallClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = FirewallClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "whelk"

    expected = "folders/{folder}".format(folder=folder,)
    actual = FirewallClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "octopus",
    }
    path = FirewallClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = FirewallClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "oyster"

    expected = "organizations/{organization}".format(organization=organization,)
    actual = FirewallClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "nudibranch",
    }
    path = FirewallClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = FirewallClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "cuttlefish"

    expected = "projects/{project}".format(project=project,)
    actual = FirewallClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "mussel",
    }
    path = FirewallClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = FirewallClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "winkle"
    location = "nautilus"

    expected = "projects/{project}/locations/{location}".format(
        project=project, location=location,
    )
    actual = FirewallClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "scallop",
        "location": "abalone",
    }
    path = FirewallClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = FirewallClient.parse_common_location_path(path)
    assert expected == actual


def test_client_withDEFAULT_CLIENT_INFO():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.FirewallTransport, "_prep_wrapped_messages"
    ) as prep:
        client = FirewallClient(
            credentials=credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.FirewallTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = FirewallClient.get_transport_class()
        transport = transport_class(
            credentials=credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)
