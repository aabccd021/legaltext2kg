from __future__ import annotations
from typing import Iterable, Union
from dataclasses import dataclass


@dataclass(frozen=True)
class PointContent:
    key: str
    isi: PointContentType


@dataclass(frozen=True)
class Point:
    description: Iterable[str]
    isi: Iterable[PointContent]


PointContentType = Union[Iterable[str], Point]


@ dataclass(frozen=True)
class Ayat:
    key: str
    isi: PointContentType


PasalContent = Union[Iterable[Ayat], PointContentType]


@ dataclass(frozen=True)
class Pasal:
    key: str
    isi: PasalContent


@ dataclass(frozen=True)
class Paragraf:
    key: str
    judul: Iterable[str]
    isi: Iterable[Pasal]


BagianContent = Union[Iterable[Paragraf], Iterable[Pasal]]


@ dataclass(frozen=True)
class Bagian:
    key: Iterable[str]
    judul: Iterable[str]
    isi: BagianContent


BabContent = Union[Iterable[Bagian], Iterable[Pasal]]


@ dataclass(frozen=True)
class Bab:
    key: Iterable[str]
    isi: BabContent


@ dataclass(frozen=True)
class LegalDocument:
    penjelasan: Iterable[str]
    pengesahan: Iterable[str]
    metadata: Iterable[str]
    babs: Iterable[Bab]
