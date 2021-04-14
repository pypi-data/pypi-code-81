import attr
from enum import Enum
from typing import List

from rbv.mk import MK


class Fakultas(Enum):
    FE = "FE"
    FHISIP = "FHISIP"
    FKIP = "FKIP"
    FST = "FST"
    PASCASARJANA = "PASCASARJANA"

    def __str__(self):
        if self.value == "FE":
            return "Fakultas Ekonomi"
        if self.value == "FHISIP":
            return "Fakultas Hukum, Ilmu Sosial, dan Ilmu Politik"
        if self.value == "FKIP":
            return "Fakultas Keguruan dan Ilmu Pendidikan"
        if self.value == "FST":
            return "Fakultas Sains dan Teknologi"
        if self.value == "PASCASARJANA":
            return "Program Pascasarjana"
        return super().__str__()


class Jenjang(Enum):
    D2 = "D2"
    D3 = "D3"
    D4 = "D4"
    S1 = "S1"
    S2 = "S2"


@attr.dataclass(slots=True)
class MataKuliah:
    nama: str
    fakultas: Fakultas
    jurusan: str
    jenjang: Jenjang
    url: str
