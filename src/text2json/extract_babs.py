
from dataclasses import dataclass
from typing import Iterable, Union
import typing
from text2json.regex import get_bab_key_int, is_bagian_start, is_pasal_start
from text2json.extract_bagians import extract_bagians
from text2json.extract_pasals import extract_pasals
from text2json.types import Bab
from text2json.utils import Extractor, extract_lines, extract_to_increment_key_list


@dataclass(frozen=True)
class DocumentMainExtraction:
    opening: Iterable[str]
    babs: Iterable[Bab]


def extract_babs(lines: Iterable[str]) -> DocumentMainExtraction:
    extracted_babs = extract_to_increment_key_list(lines, get_bab_key_int)
    opening = extracted_babs[0]
    babs_str = extracted_babs[1:]
    babs = [to_bab(s) for s in babs_str]
    return DocumentMainExtraction(
        opening=opening,
        babs=babs
    )


BabSplitType = typing.Literal["key_judul", "isi"]


def to_bab(lines: Iterable[str]) -> Bab:
    extractors = [
        Extractor[BabSplitType]("key_judul"),
        Extractor[BabSplitType]("isi", is_isi_start),
    ]
    extract_result = extract_lines(lines, extractors)
    key = get_bab_key_int(extract_result["key_judul"][0])
    assert key is not None
    judul = '\n'.join(extract_result["key_judul"][1:])
    isi_strs = extract_result["isi"]
    first_line = list(isi_strs)[0]
    isi = None
    if is_pasal_start(first_line):
        isi = extract_pasals(isi_strs)
    elif is_bagian_start(first_line):
        isi = extract_bagians(isi_strs)
    if isi == None:
        raise Exception(first_line)
    text = '\n'.join(lines)
    return Bab(_key=key, _judul=judul, isi=isi, text=text)


def is_isi_start(str: str) -> bool:
    return str != str.upper()
