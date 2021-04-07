#!/usr/bin/env python

"""Tests for `nfe.Nfe` class."""

from dataclasses import asdict
from datetime import datetime

import pytest
import pytz

from nfe_parser import nfe


@pytest.fixture()
def default_company(request):
    return nfe.Company(
        name="ACME Co.",
        state_reg="123",
        cnpj="75.315.333/0121-15",
        addr="Dummy St.",
    )


@pytest.fixture()
def default_products_list(request):
    return [
        nfe.Product(
            code="123",
            description="banana",
            qty="2.0",
            unit="UN",
            value="4.8",
            total="9.9",
        ),
        nfe.Product(
            code="124",
            description="maçã",
            qty="3.0",
            unit="UN",
            value="6.0",
            total="18.0",
        ),
    ]


@pytest.fixture()
def default_nfe(request, default_company, default_products_list):
    return nfe.Nfe(
        company=default_company,
        source="http://...",
        products=default_products_list,
        num="456",
        series="789",
        emission_date=datetime.now(tz=pytz.timezone("America/Sao_Paulo")),
        key="43181175315333012115655130000883321048579179",
        auth_protocol="143181369407004",
        cpf="111.222.333-44",
        total="27.0",
        discount="0.0",
    )


@pytest.fixture(
    params=[
        "1234 5678 9012 3456 7890 1234 5678 9012 3456 7890 1234",
        "12345678901234567890123456789012345678901234",
        "1234-5678-9012-3456-7890-1234-5678-9012-3456-7890-1234",
        "\n 12345678 9012 3456 7890 1234 5678 9012 3456 7890 1234   asd\n",
    ]
)
def key_valid(request):
    return request.param


@pytest.fixture(
    params=[
        "1234 5678 9012 3456 7890 1234 5678 9012 3456 7890 1234 5678",
        "1234 5678",
        "",
        "non-decimal-chars",
    ]
)
def key_invalid(request):
    return request.param


@pytest.fixture(
    params=[
        "123456789012345",
        "1234 5678 9012 345",
        "123-456-789-012-345",
        "\n 123456789012345   stuff\n",
    ]
)
def auth_protocol_valid(request):
    return request.param


@pytest.fixture(
    params=["123456789012345678", "1234 5678", "", "non-decimal-chars"]
)
def auth_protocol_invalid(request):
    return request.param


@pytest.fixture(
    params=["111.222.333-44", "111 222 333 44", "\n 111.222.333-44   stuff\n"]
)
def cpf_valid(request):
    return request.param


@pytest.fixture(
    params=["111.222.333-44-55", "111.222", "", "non-decimal-chars"]
)
def cpf_invalid(request):
    return request.param


@pytest.fixture(
    params=[
        "75.315.333/0121-15",
        "75315.333/0121-15",
        "75.315333/0121-15",
        "75.315.3330121-15",
        "75.315.333/012115",
        "75315333012115",
        " 75..315.333///0121-15",
    ]
)
def cnpj_valid(request):
    return request.param


@pytest.fixture(
    params=[
        "75.315.333/0121",
        "75.315.333/0121-1",
        "",
        "non-decimal-chars",
        "75.315.333/0121-15-16",
        "75.315.333/0121-19",
        "65.315.333/0121-19",
    ]
)
def cnpj_invalid(request):
    return request.param


def test_valid_nfe(default_nfe):
    nfe.Nfe(**asdict(default_nfe))


def test_valid_company_cnpj(default_company, cnpj_valid):
    default_company.cnpj = cnpj_valid


def test_invalid_company_cnpj(default_company, cnpj_invalid):
    with pytest.raises(ValueError):
        default_company.cnpj = cnpj_invalid


def test_valid_key(default_nfe, key_valid):
    default_nfe.key = key_valid


def test_invalid_key(default_nfe, key_invalid):
    with pytest.raises(ValueError):
        default_nfe.key = key_invalid


def test_valid_auth_protocol(default_nfe, auth_protocol_valid):
    default_nfe.auth_protocol = auth_protocol_valid


def test_invalid_auth_protocol(default_nfe, auth_protocol_invalid):
    with pytest.raises(ValueError):
        default_nfe.auth_protocol = auth_protocol_invalid


def test_valid_cpf(default_nfe, cpf_valid):
    default_nfe.cpf = cpf_valid


def test_invalid_cpf(default_nfe, cpf_invalid):
    with pytest.raises(ValueError):
        default_nfe.cpf = cpf_invalid
