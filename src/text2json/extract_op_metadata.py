from typing import Iterable, List, Tuple
import re
import typing
from dataclasses import dataclass
from text2json.extract_ayats import extract_point

from text2json.types import PointContentType
from text2json.utils import Extractor, compact, extract_lines_seq
from text2json.regex import *

SplitType = typing.Literal[
    "salinan",
    "name",
    "nomor_tahun",
    "tentang",
    "dengan_rahmat",
    "menimbang",
    "mengingat",
    "dengan_persetujuan",
    "memutuskan"
]


@ dataclass(frozen=True)
class OpeningMetadata:
    _name: str
    _nomor: int
    _tahun: int
    _pemutus: str
    _dengan_persetujuan: Iterable[str]
    _tentang: str
    _salinan: str
    _memutuskan: str
    menimbang: PointContentType
    mengingat: PointContentType


def extract_opening_metadata(lines: Iterable[str]) -> OpeningMetadata:
    extractors = [
        Extractor[SplitType]("salinan"),
        Extractor[SplitType]("name", name),
        Extractor[SplitType]("nomor_tahun", is_nomor),
        Extractor[SplitType]("tentang", tentang),
        Extractor[SplitType]("dengan_rahmat", pemutus),
        Extractor[SplitType]("menimbang", menimbang),
        Extractor[SplitType]("mengingat", mengingat),
        Extractor[SplitType]("dengan_persetujuan",
                             dengan_persetujuan, isOptional=True),
        Extractor[SplitType]("memutuskan", memutuskan),
    ]
    extract_result = extract_lines_seq(lines, extractors)
    nomor, tahun = extract_nomor_tahun(extract_result["nomor_tahun"])
    return OpeningMetadata(
        _salinan=" ".join(extract_result["salinan"]),
        _name=" ".join(extract_result["name"]),
        _nomor=nomor,
        _tahun=tahun,
        _tentang=extract_tentang(extract_result["tentang"]),
        _pemutus=extract_pemutus(extract_result["dengan_rahmat"]),
        menimbang=extract_menimbang(extract_result["menimbang"]),
        mengingat=extract_mengingat(extract_result["mengingat"]),
        _dengan_persetujuan=extract_dengan_persetujuan(
            extract_result["dengan_persetujuan"]),
        _memutuskan=extract_memutuskan(extract_result["memutuskan"]),
    )


def dengan_persetujuan(str: str) -> bool:
    return str == "Dengan persetujuan bersama antara"


def extract_dengan_persetujuan(strs: List[str]) -> Iterable[str]:
    strs = [x for x in strs[1:] if x != "DAN"]
    return strs


def memutuskan(str: str) -> bool:
    match = re.findall(memutuskan_re, str)
    return len(match) == 1


def extract_memutuskan(strs: List[str]) -> str:
    first_line = re.sub(memutuskan_re, "", strs[0])
    lines = compact([first_line] + strs[1:])
    return " ".join(lines)


def mengingat(str: str) -> bool:
    match = re.findall(mengingat_re, str)
    return len(match) == 1


def extract_mengingat(strs: List[str]) -> PointContentType:
    first_line = re.sub(mengingat_re, "", strs[0])
    lines = compact([first_line] + strs[1:])
    return extract_point(lines)


def menimbang(str: str) -> bool:
    match = re.findall(menimbang_re, str)
    return len(match) == 1


def extract_menimbang(strs: List[str]) -> PointContentType:
    first_line = re.sub(menimbang_re, "", strs[0])
    lines = compact([first_line] + strs[1:])
    return extract_point(lines)


def pemutus(str: str) -> bool:
    return str == "DENGAN RAHMAT TUHAN YANG MAHA ESA"


def extract_pemutus(strs: Iterable[str]) -> str:
    str = ' '.join(list(strs)[1:])
    # remove trailing comma
    return str[:-1]


def tentang(str: str) -> bool:
    return str == "TENTANG"


def extract_tentang(strs: Iterable[str]) -> str:
    return ' '.join(list(strs)[1:])


def extract_nomor_tahun(strs: Iterable[str]) -> Tuple[int, int]:
    strs = list(strs)
    if len(strs) != 1:
        raise Exception()
    str = strs[0]
    split = str.lower().replace("nomor", "").replace("tahun", "").split(" ")
    split = [x for x in split if x != '']
    return int(split[0]), int(split[1])


def name(str: str) -> bool:
    names = [
        "UNDANG-UNDANG REPUBLIK INDONESIA",
        "PERATURAN GUBERNUR",
    ]
    return any([str.startswith(name) for name in names])


def is_nomor(str: str) -> bool:
    return str.startswith("NOMOR")
