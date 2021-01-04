import re
from typing import Union
import roman

from text2json.utils import represents_int


def is_penjelasan_start(line: str) -> bool:
    return line.startswith("P E N J E L A S A N")


def is_pengesahan_start(line: str) -> bool:
    if line.startswith("Disahkan"):
        return True
    if line.startswith("Ditetapkan"):
        return True
    return False


# bab


def get_bab_key_int(str: str) -> Union[None, int]:
    if not str.startswith("BAB "):
        return None
    number = roman.fromRoman(str[4:])
    return number


# bagian
def is_bagian_start(str: str) -> bool:
    return get_bagian_key_int(str) == 1


def get_bagian_key_int(str: str) -> Union[None, int]:
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


# pasal


def is_pasal_start(str: str) -> bool:
    return get_pasal_key_int(str) is not None


def get_pasal_key_int(str: str) -> Union[int, None]:
    if str.startswith("Pasal ") and represents_int(str[6:]):
        return int(str[6:])
    return None


# paragraf
def is_paragraf_start(line: str) -> bool:
    return get_paragraf_key_int(line) == 1


def get_paragraf_key_int(str: str) -> Union[None, int]:
    splits = str.split(" ")
    if len(splits) == 2 and splits[0] == "Paragraf" and represents_int(splits[1]):
        return int(splits[1])
    return None


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


def get_num_key(num: int) -> int:
    return num


# alphabet point
alpha_regex = r'^[a-z][\.\)]'


def is_alphabet_point_start(line: str) -> bool:
    return get_alpha_key_int(line) == 97


def get_alpha_key_int(str: str) -> Union[int, None]:
    match = re.findall(alpha_regex, str)
    assert len(match) <= 1
    if len(match) == 0:
        return None
    num_str = match[0][0]
    return ord(num_str)


def get_alpha_key(num: int) -> str:
    return chr(num)


# metadata
menimbang_re = r'^Menimbang\s*:\s*'
mengingat_re = r'^Mengingat\s*:\s*'
memutuskan_re = r'^MEMUTUSKAN\s*:\s*'

# pengesahan
tempat_ditetapkan_re = r'^Ditetapkan di '
pada_tanggal_re = r'^pada tanggal '
tempat_disahkan_re = r'^Disahkan di '
jabatan_pengesah_re = r'^(GUBERNUR|PRESIDEN)'
ttd_re = r'^ttd$'
tempat_diundangkan_re = r'^Diundangkan di '
sekretaris_re = r'^SEKRETARIS '
sekretaris_re = r'^SEKRETARIS '
pengesahan_doc_re = r'^(LEMBARAN NEGARA|BERITA DAERAH) '
pengesahan_etc_re = r'^Salinan'
