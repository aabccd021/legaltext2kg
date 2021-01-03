import re
from typing import Union


def is_pasal_start(str: str) -> bool:
    return str.startswith("Pasal ")


def is_paragraf_start(str: str) -> bool:
    return str.startswith("Paragraf ")


def is_bagian_start(str: str) -> bool:
    return str.startswith("Bagian ")


def is_penjelasan_start(line: str) -> bool:
    return line.startswith("P E N J E L A S A N")


def is_pengesahan_start(line: str) -> bool:
    if line.startswith("Disahkan"):
        return True
    if line.startswith("Ditetapkan"):
        return True
    return False


# ayat point
ayat_regex = r'^\([0-9]*\)'


def is_ayat_start(line: str) -> bool:
    return get_ayat_key_int(line) == 1


def get_ayat_key_int(str: str) -> Union[int, None]:
    match = re.findall(ayat_regex, str)
    if len(match) > 1:
        raise Exception()
    if len(match) == 0:
        return None
    return int(match[0][1:-1])


# num point
num_regex = r'^[0-9]*\s*\.'


def is_num_point_start(line: str) -> bool:
    return get_num_key_int(line) == 1


def get_num_key_int(str: str) -> Union[int, None]:
    match = re.findall(num_regex, str)
    if len(match) > 1:
        raise Exception()
    if len(match) == 0:
        return None
    num_str = re.findall(r'^[0-9]*', match[0])[0]
    return int(num_str)


# alphabet point
alpha_regex = r'^[a-z][\.\)]'


def is_alphabet_point_start(line: str) -> bool:
    return get_alpha_key_int(line) == 97


def get_alpha_key_int(str: str) -> Union[int, None]:
    match = re.findall(alpha_regex, str)
    if len(match) > 1:
        raise Exception()
    if len(match) == 0:
        return None
    num_str = match[0][0]
    return ord(num_str)
