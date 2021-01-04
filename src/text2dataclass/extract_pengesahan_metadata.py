from typing import Callable, Iterable, List
import re
import typing
from dataclasses import dataclass

from text2dataclass.utils import Extractor, extract_lines_seq
from text2dataclass.regex import *

SplitType = typing.Literal[
    "tempat_disahkan",
    "tanggal_disahkan",
    "tempat_ditetapkan",
    "tanggal_ditetapkan",
    "jabatan_pengesah",
    "nama_pengesah",
    "tempat_diundangkan",
    "tanggal_diundangkan",
    "sekretaris",
    "dokumen",
    "etc"
]


@ dataclass(frozen=True)
class PengesahanMetadata:
    _text: Iterable[str]
    tempat_disahkan: str
    tanggal_disahkan: str
    tempat_ditetapkan: str
    tanggal_ditetapkan: str
    jabatan_pengesah: str
    nama_pengesah: str
    tempat_diundangkan: str
    tanggal_diundangkan: str
    sekretaris: str
    dokumen: str
    etc: Iterable[str]


def extract_pengesahan_metadata(lines: Iterable[str]) -> PengesahanMetadata:
    extractors = [
        Extractor[SplitType](
            "tempat_disahkan", found_re(tempat_disahkan_re), isOptional=True),
        Extractor[SplitType]("tanggal_disahkan",
                             found_re(pada_tanggal_re), isOptional=True),
        Extractor[SplitType]("tempat_ditetapkan",
                             found_re(tempat_ditetapkan_re), isOptional=True),
        Extractor[SplitType]("tanggal_ditetapkan",
                             found_re(pada_tanggal_re), isOptional=True),
        Extractor[SplitType]("jabatan_pengesah",
                             found_re(jabatan_pengesah_re)),
        Extractor[SplitType]("nama_pengesah", found_re(ttd_re)),
        Extractor[SplitType]("tempat_diundangkan",
                             found_re(tempat_diundangkan_re)),
        Extractor[SplitType]("tanggal_diundangkan",
                             found_re(pada_tanggal_re)),
        Extractor[SplitType]("sekretaris",
                             found_re(sekretaris_re)),
        Extractor[SplitType]("dokumen", found_re(pengesahan_doc_re)),
        Extractor[SplitType]("etc", found_re(pengesahan_etc_re))
    ]
    extract_result = extract_lines_seq(lines, extractors)
    return PengesahanMetadata(
        _text=lines,
        tempat_disahkan=del_re(tempat_disahkan_re, get_first(
            extract_result["tempat_disahkan"])),
        tanggal_disahkan=del_re(pada_tanggal_re, get_first(
            extract_result["tanggal_disahkan"])),
        tempat_ditetapkan=del_re(tempat_ditetapkan_re, get_first(
            extract_result["tempat_ditetapkan"])),
        tanggal_ditetapkan=del_re(pada_tanggal_re, get_first(
            extract_result["tanggal_ditetapkan"])),
        jabatan_pengesah=" ".join(extract_result["jabatan_pengesah"]),
        nama_pengesah=get_second(extract_result["nama_pengesah"]),
        tempat_diundangkan=del_re(tempat_diundangkan_re, get_first(
            extract_result["tempat_diundangkan"])),
        tanggal_diundangkan=del_re(pada_tanggal_re, get_first(
            extract_result["tanggal_diundangkan"])),
        sekretaris=" ".join(
            [x for x in extract_result["sekretaris"] if x != "ttd"]),
        dokumen=" ".join(extract_result["dokumen"]),
        etc=extract_result["etc"]
    )


def del_re(regex: str, str: str) -> str:
    return re.sub(regex, "", str)


def get_first(lines: List[str]) -> str:
    if len(lines) == 0:
        return ""
    if len(lines) == 1:
        return lines[0]
    raise Exception()


def get_second(lines: List[str]) -> str:
    assert len(lines) == 2
    return lines[1]


def found_re(regex: str) -> Callable[[str], bool]:
    return lambda x: len(re.findall(regex, x)) == 1
