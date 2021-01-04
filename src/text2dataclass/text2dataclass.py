from typing import Dict, List, TypeVar
import typing
from text2dataclass.extract_babs import extract_babs
from text2dataclass.extract_op_metadata import extract_opening_metadata
from text2dataclass.extract_pengesahan_metadata import extract_pengesahan_metadata
from text2dataclass.regex import is_pengesahan_start, is_penjelasan_start
from text2dataclass.types import LegalDocument

from text2dataclass.utils import Extractor, extract_lines


DocumentSplitType = typing.Literal["isi", "pengesahan", "penjelasan"]


def text2dataclass(lines: List[str]) -> LegalDocument:
    extractors = [
        Extractor[DocumentSplitType]("isi"),
        Extractor[DocumentSplitType]("penjelasan", is_penjelasan_start),
        Extractor[DocumentSplitType]("pengesahan", is_pengesahan_start),
    ]
    extract_result = extract_lines(lines, extractors)
    pengesahan = extract_result['pengesahan']
    sah = extract_pengesahan_metadata(pengesahan)
    penjelasan = extract_result['penjelasan']
    isi = extract_result['isi']
    main = extract_babs(isi)
    op = extract_opening_metadata(main.opening)

    return LegalDocument(
        _name=op._name,
        _nomor=op._nomor,
        _tahun=op._tahun,
        _pemutus=op._pemutus,
        _dengan_persetujuan=op._dengan_persetujuan,
        _tentang=op._tentang,
        _salinan=op._salinan,
        _memutuskan=op._memutuskan,
        _tempat_disahkan=sah.tempat_disahkan,
        _tanggal_disahkan=sah.tanggal_disahkan,
        _tempat_ditetapkan=sah.tempat_ditetapkan,
        _tanggal_ditetapkan=sah.tanggal_ditetapkan,
        _jabatan_pengesah=sah.jabatan_pengesah,
        _nama_pengesah=sah.nama_pengesah,
        _tempat_diundangkan=sah.tempat_diundangkan,
        _tanggal_diundangkan=sah.tanggal_diundangkan,
        _sekretaris=sah.sekretaris,
        _dokumen=sah.dokumen,
        menimbang=op.menimbang,
        mengingat=op.mengingat,
        penjelasan=penjelasan,
        pengesahan_text='\n'.join(pengesahan),
        op_text='\n'.join(main.opening),
        babs=main.babs,
    )
