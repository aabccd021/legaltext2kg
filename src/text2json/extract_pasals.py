
from text2json.extract_ayats import extract_pasal_content
from text2json.utils import extract_to_increment_key_list, represents_int
from typing import Iterable, Union
from text2json.types import Pasal


def extract_pasals(lines: Iterable[str]) -> Iterable[Pasal]:
    pasal_strs = extract_to_increment_key_list(lines, get_pasal_num)
    juduls = [x[0] for x in pasal_strs]
    ayats = [extract_pasal_content(x[1:]) for x in pasal_strs]
    return [Pasal(key=judul, isi=ayat) for judul, ayat in zip(juduls, ayats)]


def get_pasal_num(str: str) -> Union[int, None]:
    if str.startswith("Pasal ") and represents_int(str[6:]):
        return int(str[6:])
    return None
