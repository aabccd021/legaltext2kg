
from text2dataclass.extract_ayats import extract_pasal_content
from text2dataclass.regex import get_pasal_key_int
from text2dataclass.utils import extract_to_increment_key_list, represents_int
from typing import Iterable, Union
from text2dataclass.types import Pasal


def extract_pasals(lines: Iterable[str]) -> Iterable[Pasal]:
    pasal_strs = extract_to_increment_key_list(lines, get_pasal_key_int)
    # text = "\n".join(lines)
    texts = ["\n".join(x) for x in pasal_strs]
    juduls = [get_pasal_key_int(x[0]) for x in pasal_strs]
    juduls = [x for x in juduls if x is not None]
    ayats = [extract_pasal_content(x[1:]) for x in pasal_strs]
    assert len(juduls) == len(ayats)
    return [Pasal(_key=judul, isi=ayat, text=text) for judul, ayat, text in zip(juduls, ayats, texts)]
