# import pathlib
import re
import textwrap
from dataclasses import dataclass
from datetime import datetime
from typing import List

import rich
from rich import box
from rich.console import RenderGroup
from rich.padding import Padding
from rich.panel import Panel
from rich.table import Table
from rich.text import Text


@dataclass
class Product:
    code: str
    description: str
    unit: str

    def setqty(self, v):
        if isinstance(v, float):
            self.__dict__["qty"] = v
            return
        try:
            self.__dict__["qty"] = float(v.replace(",", "."))
        except ValueError:
            raise ValueError(
                f"Product qty must be a string representing a float, with "
                f"a comma, e.g: XX,YY, instead got: {v}"
            )

    def getqty(self):
        return self.__dict__.get("qty")

    qty: property = property(getqty, setqty)
    del setqty, getqty

    def setvalue(self, v):
        if isinstance(v, float):
            self.__dict__["value"] = v
            return
        try:
            self.__dict__["value"] = float(v.replace(",", "."))
        except ValueError:
            raise ValueError(
                f"Product value must be a string representing a float, with "
                f"a comma, e.g: XX,YY, instead got: {v}"
            )

    def getvalue(self):
        return self.__dict__.get("value")

    value: property = property(getvalue, setvalue)
    del setvalue, getvalue

    def settotal(self, v):
        if isinstance(v, float):
            self.__dict__["total"] = v
            return
        try:
            self.__dict__["total"] = float(v.replace(",", "."))
        except ValueError:
            raise ValueError(
                f"Product total must be a string representing a float, with "
                f"a comma, e.g: XX,YY, instead got: {v}"
            )

    def gettotal(self):
        return self.__dict__.get("total")

    total: property = property(gettotal, settotal)
    del settotal, gettotal


@dataclass
class Company:
    name: str
    state_reg: str
    addr: str

    def setcnpj(self, v: str):
        if not isinstance(v, str):
            raise TypeError(...)
        v = re.sub(r"[^\d]*", "", v)  # remove everything that is non decimal
        if not re.match(r"^\d{14}$", v):
            raise ValueError(
                "Cnpj must be a string with 14 decimal numbers (non decimal "
                "characters are discarded), e.g format: XX.XXX.XXX/YYYY-ZZ"
            )
        self.__dict__["cnpj"] = v
        if not self.validate_cnpj(v):
            raise ValueError("Cnpj failed the validation algorithm")

    def getcnpj(self):
        return self.__dict__.get("cnpj")

    cnpj: property = property(getcnpj, setcnpj)
    del setcnpj, getcnpj

    def validate_cnpj(self, cnpj) -> bool:
        # implementation according to:
        # https://pt.wikipedia.org/wiki/Cadastro_Nacional_da_Pessoa_Jur%C3%ADdica
        vs = [int(v) for v in cnpj]

        # check the first verification number
        c1 = 5 * vs[0] + 4 * vs[1] + 3 * vs[2] + 2 * vs[3]
        c1 += 9 * vs[4] + 8 * vs[5] + 7 * vs[6] + 6 * vs[7]
        c1 += 5 * vs[8] + 4 * vs[9] + 3 * vs[10] + 2 * vs[11]
        c1 = 11 - c1 % 11
        c1 = 0 if c1 > 9 else c1

        # check the second verification number
        c2 = 6 * vs[0] + 5 * vs[1] + 4 * vs[2] + 3 * vs[3]
        c2 += 2 * vs[4] + 9 * vs[5] + 8 * vs[6] + 7 * vs[7]
        c2 += 6 * vs[8] + 5 * vs[9] + 4 * vs[10] + 3 * vs[11]
        c2 += 2 * vs[12]
        c2 = 11 - c2 % 11
        c2 = 0 if c2 > 9 else c2

        return c1 == vs[12] and c2 == vs[13]


@dataclass
class Nfe:
    company: Company
    source: str
    products: List[Product]
    num: str
    series: str
    emission_date: datetime

    def setkey(self, v: str):
        v = re.sub(r"[^\d]*", "", v)  # remove everything that is non decimal
        if not re.match(r"^\d{44}$", v):
            raise ValueError(
                "Access key must be a string with 44 decimal numbers (non"
                "decimal characters are discarded), e.g format: "
                "1234 5678 9012 3456 7890 1234 5678 9012 3456 7890 1234"
            )
        self.__dict__["key"] = v

    def getkey(self):
        return self.__dict__.get("key")

    key: property = property(getkey, setkey)
    del setkey, getkey

    def setauthprotocol(self, v: str):
        v = re.sub(r"[^\d]*", "", v)  # remove everything that is non decimal
        if not re.match(r"^\d{15}$", v):
            raise ValueError(
                "Authorization protocol must be a string with 15 decimal "
                "numbers (non decimal characters are discarded), e.g format: "
                "123456789012345"
            )
        self.__dict__["auth_protocol"] = v

    def getauthprotocol(self):
        return self.__dict__.get("auth_protocol")

    auth_protocol: property = property(getauthprotocol, setauthprotocol)
    del setauthprotocol, getauthprotocol

    def setcpf(self, v: str):
        v = re.sub(r"[^\d]*", "", v)  # remove everything that is non decimal
        if not re.match(r"^\d{11}$", v):
            raise ValueError(
                "Cpf must be a string with 11 decimal numbers (non decimal "
                "characters are discarded), e.g format: XXX.XXX.XXX-YY"
            )
        self.__dict__["cpf"] = v

    def getcpf(self):
        return self.__dict__.get("cpf")

    cpf: property = property(getcpf, setcpf)
    del setcpf, getcpf

    def settotal(self, v):
        if isinstance(v, float):
            self.__dict__["total"] = v
            return
        try:
            self.__dict__["total"] = float(v.replace(",", "."))
        except ValueError:
            raise ValueError(
                f"Product total must be a string representing a float, with "
                f"a comma, e.g: XX,YY, instead got: {v}"
            )

    def gettotal(self):
        return self.__dict__.get("total")

    total: property = property(gettotal, settotal)
    del settotal, gettotal

    def setdiscount(self, v):
        if isinstance(v, float):
            self.__dict__["discount"] = v
            return
        try:
            self.__dict__["discount"] = float(v.replace(",", "."))
        except ValueError:
            raise ValueError(
                f"Product discount must be a string representing a float, with "
                f"a comma, e.g: XX,YY, instead got: {v}"
            )

    def getdiscount(self):
        return self.__dict__.get("discount")

    discount: property = property(getdiscount, setdiscount)
    del setdiscount, getdiscount


def print(nfe: Nfe):

    nfe_group = RenderGroup(
        Text(
            " ".join(textwrap.wrap(nfe.key, 4)),
            style="bold black",
            justify="center",
        ),
        Text(f"NFC-e no. {nfe.num}", style="black", justify="center"),
        Text(
            f"Emission date: {nfe.emission_date}",
            style="black",
            justify="center",
        ),
        Text(
            f"Auth. protocol: {nfe.auth_protocol}",
            style="black",
            justify="center",
        ),
    )

    company_panel = Panel(
        RenderGroup(
            Text(f"CNPJ: {nfe.company.cnpj}", style="black", justify="center",),
            Text(
                f"State Registration: {nfe.company.state_reg}",
                style="black",
                justify="center",
            ),
            Text(f"{nfe.company.addr}", style="black", justify="center"),
        ),
        title="[blue][b]Company",
    )

    cpf = nfe.cpf
    consumer_panel = Panel(
        RenderGroup(
            Text(
                f"CPF: {cpf[0:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:12]}",
                style="black",
                justify="center",
            ),
        ),
        title="[blue][b]Consumer",
    )

    footer = RenderGroup(
        Text(f"Total: {nfe.total}", style="black", justify="right"),
        Text(f"Discount: {nfe.discount}", style="black", justify="right"),
    )

    pt = Table(box=box.SIMPLE)
    pt.add_column("Code", justify="left", style="black", no_wrap=True)
    pt.add_column("Description", justify="left", style="black", no_wrap=True)
    pt.add_column("Qty", justify="center", style="black", no_wrap=True)
    pt.add_column("Unit", justify="center", style="black", no_wrap=True)
    pt.add_column("Val/unit", justify="right", style="black", no_wrap=True)
    pt.add_column("Partial", justify="right", style="black", no_wrap=True)

    for p in nfe.products:
        pt.add_row(
            p.code,
            p.description,
            str(p.qty),
            p.unit,
            str(p.value),
            str(p.total),
        )

    products_panel = Panel(RenderGroup(pt, footer), title="[blue][b]Products")

    main_panel = Panel(
        RenderGroup(nfe_group, company_panel, consumer_panel, products_panel),
        title="[blue][b]NFC-e",
        expand=False,
        style="black on khaki1",
        box=box.SQUARE,
    )

    rich.print(Padding(main_panel, 1))
