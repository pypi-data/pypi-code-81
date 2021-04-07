"""Main module."""

import os
import pathlib
import re
import sys
import time
from datetime import datetime
from http import cookiejar
from typing import Any, Callable, Dict, Tuple, TypedDict

import fake_useragent
import requests

from nfe_parser import nfe


class ParserArgs(TypedDict):
    pattern: str
    key: Callable


parser_args: Dict[str, ParserArgs] = {
    "url": {
        "pattern": (
            r'<iframe\s*id="iframeConteudo" class="iframe".*?'
            r'src="(?P<url>.*?)">.*?</iframe>'
        ),
        "key": str,
    },
    "co_name": {
        "pattern": (
            r'<td class="NFCCabecalho_SubTitulo"'
            r'\s+align="left">(?P<co_name>.*?)</td>'
        ),
        "key": str,
    },
    "co_state_reg": {
        "pattern": (
            r'<td class="NFCCabecalho_SubTitulo1".*?CNPJ.*?'
            r"Insc.+?Estadual:\s*(?P<state_reg>.+?)\s*?</td>"
        ),
        "key": str,
    },
    "co_cnpj": {
        "pattern": (
            r'<td class="NFCCabecalho_SubTitulo1".*?CNPJ:\s*'
            r"(?P<co_cnpj>.+?)\s*Insc.+?Estadual:.*?</td>"
        ),
        "key": str,
    },
    "co_addr": {
        "pattern": (
            r'<td class="NFCCabecalho_SubTitulo1".*?<td class='
            r'"NFCCabecalho_SubTitulo1".+?>(?P<co_addr>.+?)</td>'
        ),
        "key": lambda val: " ".join(val.split()),
    },
    "products": {
        "pattern": (
            r'<tr id="Item.+?\s+\d+">\s*'
            r'<td class="NFCDetalhe_Item".+?>(?P<code>.*?)</td>\s*?'
            r"<td.*?>(?P<description>.*?)</td>\s*?"
            r"<td.*?>(?P<qty>.*?)</td>\s*?"
            r"<td.*?>(?P<unit>.*?)</td>\s*?"
            r"<td.*?>(?P<value>.*?)</td>\s*?"
            r"<td.*?>(?P<total>.*?)</td>"
        ),
        "key": nfe.Product,
    },
    "num": {
        "pattern": (
            r'<td class="NFCCabecalho_SubTitulo" align="center">'
            r"\s+NFC-e n.:\s(?P<num>\d+).*?</td>"
        ),
        "key": int,
    },
    "series": {
        "pattern": (
            r'<td class="NFCCabecalho_SubTitulo" align="center">'
            r"\s+NFC-e.+?S.rie:\s(?P<series>\d+).*?</td>"
        ),
        "key": int,
    },
    "emission_date": {
        "pattern": (
            r'<td class="NFCCabecalho_SubTitulo" align="center">'
            r"\s+NFC-e.+?S.rie:.+?"
            r"Data de Emiss.o: (?P<emission_date>.+?)\s*</td>"
        ),
        "key": lambda val: datetime.strptime(val, "%d/%m/%Y %H:%M:%S"),
    },
    "key": {"pattern": r"(?P<key>(?:\d{4}\s){10}\d{4})", "key": str},
    "auth_protocol": {
        "pattern": (
            r"\s*Protocolo de Autoriza.?.?o:\s+"
            r"(?P<auth_protocol>\d+)\s*</td>"
        ),
        "key": str,
    },
    "cpf": {
        "pattern": (r"\s*CPF:\s*(?P<cpf>(?:\d{2,3}(?:\.|-)){3}\d{2})\s*"),
        "key": str,
    },
    "total": {
        "pattern": (
            r"\s*Valor total R.*?</td>\s*<td.*?>\s*" r"(?P<total>.*?)\s*</td>"
        ),
        "key": str,
    },
    "discount": {
        "pattern": (
            r"\s*Valor descontos R.*?</td>\s*<td.*?>\s*"
            r"(?P<total>.*?)\s*</td>"
        ),
        "key": str,
    },
}


class RequestFailedError(Exception):
    pass


class ParseError(Exception):
    pass


class BlockAll(cookiejar.CookiePolicy):
    return_ok = (
        set_ok
    ) = domain_return_ok = path_return_ok = lambda self, *args, **kwargs: False
    netscape = True
    rfc2965 = hide_cookie2 = False


def gen_user_agent() -> str:
    # redirect stderr to /dev/null so that `fake_useragent.UserAgent()`
    # method does not polute stderr (this is an unfortunate bug, already
    # reported in https://github.com/hellysmile/fake-useragent/issues/78)
    sys.stderr = open(os.devnull, "w")
    try:
        ua = fake_useragent.UserAgent(cache=True)
    except fake_useragent.errors.FakeUserAgentError:
        # something went wrong fake_useragent... just hardcode a user agent
        ua_text = (
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 "
            "(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11"
        )
    else:
        ua_text = ua.random
    finally:
        sys.stderr = sys.__stderr__
    return ua_text


def pull_html(url: str, timeout: int = 60) -> Tuple[str, str]:
    start_time = time.time()
    s = requests.Session()
    s.cookies.set_policy(BlockAll())
    ua_text = gen_user_agent()
    headers = {"User-Agent": ua_text}
    elapsed_time = time.time() - start_time
    exception: Exception = Exception()
    while elapsed_time < timeout:
        try:
            print(f"attempt request... {elapsed_time}")
            r1 = s.get(url, headers=headers)
        except requests.exceptions.ConnectionError as e:
            exception = e
        else:
            if r1.ok:
                break
            else:
                exception = RequestFailedError(
                    f"The request on {url} failed with {r1.status_code}"
                )

        elapsed_time = time.time() - start_time
        time.sleep(1)
    else:
        raise TimeoutError(
            f"The request on {url} timeout after {timeout}s and failed with "
            f" {type(exception).__class__}: {exception}"
        )

    return (r1.text, r1.encoding)


def parse_token(token: str, data: str) -> Any:
    patt: str = parser_args[token]["pattern"]
    key: Callable = parser_args[token]["key"]

    m = re.finditer(patt, data, re.DOTALL)
    ml = list(m)
    if not ml and token != "cpf":  # cpf is not mandatory
        raise ParseError(
            f"Unable to find pattern '{patt}' while looking for '{token}'"
        )

    # edge case: when there is no cpf
    if len(ml) == 0 and token == "cpf":
        ret = key("00000000000")
    # edge case: ensure a products list with one item is not handled here
    elif len(ml) == 1 and token != "products":
        ret = key(ml[0].group(1))
    else:
        ret = [key(**m.groupdict()) for m in ml]
    return ret


def parse_nfe_from_url(url: str) -> nfe.Nfe:
    (data, encoding) = pull_html(url)
    url = parse_token("url", data)
    (data, encoding) = pull_html(url)
    args = {
        k: parse_token(k, data)
        for k, _ in parser_args.items()
        if k != "url" and not k.startswith("co_")
    }
    co = {
        k.split("_", 1)[1]: parse_token(k, data)
        for k, v in parser_args.items()
        if k.startswith("co_")
    }
    company = nfe.Company(**co)
    return nfe.Nfe(company=company, source=url, **args)


def parse_nfe_from_file(path: str, encoding: str = "iso-8859-1") -> nfe.Nfe:
    data: str = pathlib.Path(path).read_text(encoding=encoding)
    args = {
        k: parse_token(k, data)
        for k, _ in parser_args.items()
        if k != "url" and not k.startswith("co_")
    }
    co = {
        k.split("_", 1)[1]: parse_token(k, data)
        for k, v in parser_args.items()
        if k.startswith("co_")
    }
    company = nfe.Company(**co)
    return nfe.Nfe(company=company, source=path, **args)
