from typing import Iterable, List, Union
import typing
from text2dataclass.regex import get_bagian_key_int, is_paragraf_start, is_pasal_start
from text2dataclass.extract_paragraphs import extract_paragraf
from text2dataclass.extract_pasals import extract_pasals

from text2dataclass.types import Bagian
from text2dataclass.utils import Extractor, extract_lines, extract_to_increment_key_list


def extract_bagians(lines: Iterable[str]) -> Iterable[Bagian]:
    pasal_strs = extract_to_increment_key_list(lines, get_bagian_key_int)
    return [to_bagian(x) for x in pasal_strs]


BabSplitType = typing.Literal["judul", "isi"]


def to_bagian(lines: List[str]) -> Bagian:
    text = '\n'.join(lines)
    key = get_bagian_key_int(lines[0])
    assert key is not None
    extractors = [
        Extractor[BabSplitType]("judul"),
        Extractor[BabSplitType]("isi", is_isi_start),
    ]
    extract_result = extract_lines(lines[1:], extractors)
    judul_strs = ' '.join(extract_result["judul"])
    isi_strs = extract_result["isi"]
    first_line = list(isi_strs)[0]
    isi = None
    if is_pasal_start(first_line):
        isi = extract_pasals(isi_strs)
    elif is_paragraf_start(first_line):
        isi = extract_paragraf(isi_strs)
    if isi == None:
        raise Exception(isi)
    return Bagian(_key=key, _judul=judul_strs, isi=isi, text=text)


def is_isi_start(str: str) -> bool:
    return is_pasal_start(str) or is_paragraf_start(str)
