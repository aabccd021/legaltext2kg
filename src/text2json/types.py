from __future__ import annotations
from typing import Iterable, Union, Literal
from dataclasses import dataclass


@dataclass(frozen=True)
class PointContent:
    _key: Union[str, int]
    isi: PointContentType
    _type: Literal['point'] = 'point'


@dataclass(frozen=True)
class Point:
    _description: str
    isi: Iterable[PointContent]
    text: str
    _type: Literal['points'] = 'points'


PointContentType = Union[Iterable[str], Point, str]


@ dataclass(frozen=True)
class Ayat:
    _key: int
    isi: PointContentType
    _type: Literal['ayat'] = 'ayat'


PasalContent = Union[Iterable[Ayat], PointContentType]


@ dataclass(frozen=True)
class Pasal:
    _key: int
    isi: PasalContent
    text: str
    _type: Literal['pasal'] = 'pasal'


@ dataclass(frozen=True)
class Paragraf:
    _key: int
    _judul: str
    isi: Iterable[Pasal]
    text: str
    _type: Literal['paragraf'] = 'paragraf'


BagianContent = Union[Iterable[Paragraf], Iterable[Pasal]]


@ dataclass(frozen=True)
class Bagian:
    _key: int
    _judul: str
    isi: BagianContent
    text: str
    _type: Literal['bagian'] = 'bagian'


BabContent = Union[Iterable[Bagian], Iterable[Pasal]]


@ dataclass(frozen=True)
class Bab:
    _key: int
    _judul: str
    isi: BabContent
    text: str
    _type: Literal['bab'] = 'bab'


@ dataclass(frozen=True)
class Metadata:
    _name: str
    _nomor: int
    _tahun: int
    _pemutus: str
    _dengan_persetujuan: Iterable[str]
    _tentang: str
    _salinan: str
    _memutuskan: str
    _tempat_disahkan: str
    _tanggal_disahkan: str
    _tempat_ditetapkan: str
    _tanggal_ditetapkan: str
    _jabatan_pengesah: str
    _nama_pengesah: str
    _tempat_diundangkan: str
    _tanggal_diundangkan: str
    _sekretaris: str
    _dokumen: str
    menimbang: PointContentType
    mengingat: PointContentType


@ dataclass(frozen=True)
class LegalDocument:
    penjelasan: Iterable[str]
    _metadata: Metadata
    pengesahan_text: str
    op_text: str
    babs: Iterable[Bab]
