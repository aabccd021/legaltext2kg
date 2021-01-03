import re
from typing import Callable, Iterable, List, Tuple, Union
import typing
from text2json.regex import *

from text2json.types import Ayat, PasalContent, Point, PointContent, PointContentType
from text2json.utils import Extractor, extract_lines, extract_to_increment_key_list, represents_int


PointSplitType = typing.Literal["description", "isi"]


def extract_pasal_content(lines: Iterable[str]) -> PasalContent:
    # extract ayat
    if list(lines)[0].startswith('(1)'):
        ayat_strs = extract_to_increment_key_list(lines, get_ayat_key_int)
        keys, contents = extract_prefixed_keys(ayat_strs, ayat_regex)
        contents = [extract_point(c) for c in contents]
        return [Ayat(key=key, isi=isi) for key, isi in zip(keys, contents)]
    return extract_point(lines)


def extract_point(lines: Iterable[str]) -> PointContentType:
    # num points
    for line in lines:
        if is_num_point_start(line):
            return extract_point_u(
                lines,
                is_num_point_start,
                get_num_key_int,
                num_regex
            )
        # alphabet points
        if is_alphabet_point_start(line):
            return extract_point_u(
                lines,
                is_alphabet_point_start,
                get_alpha_key_int,
                alpha_regex
            )

    return lines


def extract_point_u(
    lines: Iterable[str],
    func: Callable[[str], bool],
    func2: Callable[[str], Union[int, None]],
    regex: str
) -> Point:
    extractors = [
        Extractor[PointSplitType]("description"),
        Extractor[PointSplitType]("isi", func),
    ]
    extract_result = extract_lines(lines, extractors)
    desc_strs = extract_result["description"]
    isi_strs = extract_result["isi"]
    point_content_strs = extract_to_increment_key_list(
        isi_strs, func2)
    keys, contents = extract_prefixed_keys(point_content_strs, regex)
    contents = [extract_point(c) for c in contents]

    point_content = [PointContent(key, content) for key, content
                     in zip(keys, contents)]
    return Point(description=desc_strs, isi=point_content)


def extract_prefixed_keys(strs: List[List[str]], regex: str) -> Tuple[List[str], List[List[str]]]:
    keys = [re.findall(regex, x[0])[0] for x in strs]
    contents = [[re.sub(regex, "", x[0]).strip()] + x[1:]
                for x in strs]
    contents = [[z for z in x if z != ""] for x in contents]
    return keys, contents
