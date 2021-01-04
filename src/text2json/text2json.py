from typing import Dict, List, TypeVar
import typing
from text2json.extract_babs import extract_babs
from text2json.extract_op_metadata import extract_opening_metadata
from text2json.merge_metadata import merge_metadata
from text2json.regex import is_pengesahan_start, is_penjelasan_start
from text2json.types import LegalDocument

from text2json.utils import Extractor, extract_lines


DocumentSplitType = typing.Literal["isi", "pengesahan", "penjelasan"]


def text2json(lines: List[str]) -> LegalDocument:
    extractors = [
        Extractor[DocumentSplitType]("isi"),
        Extractor[DocumentSplitType]("penjelasan", is_penjelasan_start),
        Extractor[DocumentSplitType]("pengesahan", is_pengesahan_start),
    ]
    extract_result = extract_lines(lines, extractors)
    pengesahan = extract_result['pengesahan']
    penjelasan = extract_result['penjelasan']
    isi = extract_result['isi']
    main = extract_babs(isi)
    op_metadata = extract_opening_metadata(main.opening)

    return LegalDocument(
        penjelasan=penjelasan,
        pengesahan=pengesahan,
        _metadata=merge_metadata(op_metadata),
        babs=main.babs
    )
