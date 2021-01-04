from text2json.extract_op_metadata import OpeningMetadata
from text2json.types import Metadata


def merge_metadata(op: OpeningMetadata) -> Metadata:
    return Metadata(
        _name=op._name,
        _nomor=op._nomor,
        _tahun=op._tahun,
        _pemutus=op._pemutus,
        _dengan_persetujuan=op._dengan_persetujuan,
        _tentang=op._tentang,
        _salinan=op._salinan,
        _memutuskan=op._memutuskan,
        menimbang=op.menimbang,
        mengingat=op.mengingat,
    )
