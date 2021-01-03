from typing import Iterable, List, Union
import typing
from text2json.regex import is_pasal_start
from text2json.extract_pasals import extract_pasals
from text2json.types import Paragraf

from text2json.utils import Extractor, extract_lines, extract_to_increment_key_list, represents_int


def get_paragraf_num(str: str) -> Union[None, int]:
    splits = str.split(" ")
    if len(splits) == 2 and splits[0] == "Paragraf" and represents_int(splits[1]):
        return int(splits[1])
    return None


def extract_paragraf(lines: Iterable[str]) -> Iterable[Paragraf]:
    pasal_strs = extract_to_increment_key_list(lines, get_paragraf_num)
    return [to_paragraf(x) for x in pasal_strs]


BabSplitType = typing.Literal["judul", "isi"]


def to_paragraf(paragraf_str: List[str]) -> Paragraf:
    key = paragraf_str[0]
    extractors = [
        Extractor[BabSplitType]("judul"),
        Extractor[BabSplitType]("isi", is_isi_start),
    ]
    extract_result = extract_lines(paragraf_str[1:], extractors)
    judul_strs = extract_result["judul"]
    isi_strs = extract_result["isi"]
    first_line = list(isi_strs)[0]
    isi = None
    if is_pasal_start(first_line):
        isi = extract_pasals(isi_strs)

    if isi == None:
        raise Exception(isi)
    return Paragraf(key=key, judul=judul_strs, isi=isi)


def is_isi_start(str: str) -> bool:
    return is_pasal_start(str)
