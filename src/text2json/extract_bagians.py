from typing import Iterable, List, Union
import typing
from text2json.regex import is_paragraf_start, is_pasal_start
from text2json.extract_paragraphs import extract_paragraf
from text2json.extract_pasals import extract_pasals

from text2json.types import Bagian
from text2json.utils import Extractor, extract_lines, extract_to_increment_key_list


def get_bagian_num(str: str) -> Union[None, int]:
    if not str.startswith("Bagian "):
        return None
    number_str = str[7:]
    if number_str == "Kesatu":
        return 1
    if number_str == "Pertama":
        return 1
    if number_str == "Kedua":
        return 2
    if number_str == "Ketiga":
        return 3
    if number_str == "Keempat":
        return 4
    if number_str == "Kelima":
        return 5
    if number_str == "Keenam":
        return 6
    if number_str == "Ketujuh":
        return 7
    if number_str == "Kedelapan":
        return 8
    if number_str == "Kesembilan":
        return 9
    raise Exception(str)


def extract_bagians(lines: Iterable[str]) -> Iterable[Bagian]:
    pasal_strs = extract_to_increment_key_list(lines, get_bagian_num)
    return [to_bagian(x) for x in pasal_strs]


BabSplitType = typing.Literal["judul", "isi"]


def to_bagian(bagian_str: List[str]) -> Bagian:
    key = bagian_str[0]
    extractors = [
        Extractor[BabSplitType]("judul"),
        Extractor[BabSplitType]("isi", is_isi_start),
    ]
    extract_result = extract_lines(bagian_str[1:], extractors)
    judul_strs = extract_result["judul"]
    isi_strs = extract_result["isi"]
    first_line = list(isi_strs)[0]
    isi = None
    if is_pasal_start(first_line):
        isi = extract_pasals(isi_strs)
    elif is_paragraf_start(first_line):
        isi = extract_paragraf(isi_strs)

    if isi == None:
        raise Exception(isi)
    return Bagian(key=key, judul=judul_strs, isi=isi)


def is_isi_start(str: str) -> bool:
    return is_pasal_start(str) or is_paragraf_start(str)
