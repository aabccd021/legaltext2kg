import dataclasses
from typing import Callable, Dict, Generic, Iterable, List, TypeVar, Union


def default_extractor_func(_: str): return False


T = TypeVar('T')


@dataclasses.dataclass
class Extractor(Generic[T]):
    name: T
    func: Callable[[str], bool] = default_extractor_func


U = TypeVar('U')


def extract_lines(lines: Iterable[str], extractors: List[Extractor[U]]) -> Dict[U, Iterable[str]]:
    current_extractor = extractors[0]
    result = {extractor.name: [] for extractor in extractors}
    for line in lines:
        for next_extractor_candidate in extractors:
            if next_extractor_candidate.func(line):
                current_extractor = next_extractor_candidate
        result[current_extractor.name].append(line)
    return result


def extract_to_increment_key_list(
    lines: Iterable[str],
    is_start_fn: Callable[[str], Union[int, None]],
) -> List[List[str]]:
    elements: List[List[str]] = [[]]
    prev_cnt: Union[None, int] = None
    for line in lines:
        is_start = False
        cur_cnt = is_start_fn(line)
        if cur_cnt != None:
            if prev_cnt != None:
                is_start = cur_cnt == prev_cnt + 1
            else:
                is_start = True
            if is_start:
                prev_cnt = cur_cnt

        if is_start:
            elements.append([])
        elements[-1].append(line)
    elements_without_empty = [e for e in elements if e != []]
    return elements_without_empty


def represents_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
