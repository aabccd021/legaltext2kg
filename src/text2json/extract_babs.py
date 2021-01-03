
from dataclasses import dataclass
from typing import Iterable, Union
import typing
from text2json.regex import is_bagian_start, is_pasal_start
from text2json.extract_bagians import extract_bagians
from text2json.extract_pasals import extract_pasals
from text2json.types import Bab
from text2json.utils import Extractor, extract_lines, extract_to_increment_key_list
import roman


@dataclass(frozen=True)
class DocumentMainExtraction:
    metadata: Iterable[str]
    babs: Iterable[Bab]


def get_bab_num(str: str) -> Union[None, int]:
    if not str.startswith("BAB "):
        return None
    number = roman.fromRoman(str[4:])
    return number


def extract_babs(lines: Iterable[str]) -> DocumentMainExtraction:
    extracted_babs = extract_to_increment_key_list(lines, get_bab_num)
    metadata = extracted_babs[0]
    babs_str = extracted_babs[1:]
    babs = [to_bab(s) for s in babs_str]
    return DocumentMainExtraction(
        metadata=metadata,
        babs=babs
    )


BabSplitType = typing.Literal["judul", "isi"]


def to_bab(babs_str: Iterable[str]) -> Bab:
    extractors = [
        Extractor[BabSplitType]("judul"),
        Extractor[BabSplitType]("isi", is_isi_start),
    ]
    extract_result = extract_lines(babs_str, extractors)
    judul_strs = extract_result["judul"]
    isi_strs = extract_result["isi"]
    first_line = list(isi_strs)[0]
    isi = None
    if is_pasal_start(first_line):
        isi = extract_pasals(isi_strs)
    elif is_bagian_start(first_line):
        isi = extract_bagians(isi_strs)

    if isi == None:
        raise Exception(isi)
    return Bab(key=judul_strs, isi=isi)


def is_isi_start(str: str) -> bool:
    return str != str.upper()
