import re
from typing import Callable, Iterable, List, Tuple, Union
import typing
from text2dataclass.regex import *

from text2dataclass.types import Ayat, PasalContent, Points, Point, StrsOrPoints
from text2dataclass.utils import Extractor, compact, extract_lines, extract_to_increment_key_list


PointSplitType = typing.Literal["description", "isi"]


def extract_pasal_content(lines: Iterable[str]) -> PasalContent:
    # extract ayat
    if is_ayat_start(list(lines)[0]):
        ayat_strs = extract_to_increment_key_list(lines, get_ayat_key_int)
        texts = ["\n".join(x) for x in ayat_strs]
        keys, contents = extract_prefixed_keys(ayat_strs, ayat_regex)
        keys = [get_ayat_key_int(x) for x in keys]
        keys = [x for x in keys if x is not None]
        contents = [extract_point(c) for c in contents]
        assert len(keys) == len(contents)
        return [Ayat(_key=key, isi=isi, text=text) for key, isi, text in zip(keys, contents, texts)]
    return extract_point(lines)


def extract_point(lines: Iterable[str]) -> StrsOrPoints:
    # num points
    for line in lines:
        if is_num_point_start(line):
            return extract_point_u(
                lines,
                is_num_point_start,
                get_num_key_int,
                get_num_key,
                num_regex
            )
        # alphabet points
        if is_alphabet_point_start(line):
            return extract_point_u(
                lines,
                is_alphabet_point_start,
                get_alpha_key_int,
                get_alpha_key,
                alpha_regex
            )

    return ' '.join(lines)


def extract_point_u(
    lines: Iterable[str],
    is_start: Callable[[str], bool],
    get_key_int: Callable[[str], Union[int, None]],
    get_key: Callable[[int], Union[int, str]],
    regex: str
) -> Points:
    extractors = [
        Extractor[PointSplitType]("description"),
        Extractor[PointSplitType]("isi", is_start),
    ]
    extract_result = extract_lines(lines, extractors)
    desc_str = "\n".join(extract_result["description"])
    isi_strs = extract_result["isi"]
    point_content_strs = extract_to_increment_key_list(
        isi_strs, get_key_int)
    keys, contents = extract_prefixed_keys(point_content_strs, regex)
    keys = [get_key_int(x) for x in keys]
    keys = [get_key(x) for x in keys if x is not None]
    contents = [extract_point(c) for c in contents]
    assert len(keys) == len(contents)
    texts = ["\n".join(x) for x in point_content_strs]
    point_content = [Point(_key=key, isi=content, text=text) for key, content, text
                     in zip(keys, contents, texts)]
    text = "\n".join(lines)
    return Points(
        _description=desc_str,
        isi=point_content,
        text=text
    )


def extract_prefixed_keys(strs: List[List[str]], regex: str) -> Tuple[List[str], List[List[str]]]:
    keys = [re.findall(regex, x[0])[0] for x in strs]
    contents = [[re.sub(regex, "", x[0]).strip()] + x[1:]
                for x in strs]
    contents = [list(compact(x)) for x in contents]
    return keys, contents
