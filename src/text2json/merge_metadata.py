from text2json.extract_op_metadata import OpeningMetadata
from text2json.extract_pengesahan_metadata import PengesahanMetadata
from text2json.types import Metadata


def merge_metadata(op: OpeningMetadata, sah: PengesahanMetadata) -> Metadata:
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
        _tempat_disahkan=sah.tempat_disahkan,
        _tanggal_disahkan=sah.tanggal_disahkan,
        _tempat_ditetapkan=sah.tempat_ditetapkan,
        _tanggal_ditetapkan=sah.tanggal_ditetapkan,
        _jabatan_pengesah=sah.jabatan_pengesah,
        _nama_pengesah=sah.nama_pengesah,
        _tempat_diundangkan=sah.tempat_diundangkan,
        _tanggal_diundangkan=sah.tanggal_diundangkan,
        _sekretaris=sah.sekretaris,
        _dokumen=sah.dokumen
    )
