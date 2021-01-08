# pyright: reportGeneralTypeIssues
from typing import List, Tuple
from rdflib.namespace import NamespaceManager
from rdflib.term import Literal, Node
from dataclass2rdf.get_bab_triple import babs_to_triple
from dataclass2rdf.get_strs_or_points_triple import point_content_to_triple
from dataclass2rdf.types import Triples
from text2dataclass.types import LegalDocument
from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import XSD, RDF
from dataclass2rdf.utils import *
import itertools


def dataclass2triples(doc: LegalDocument, doc_name: str) -> List[Tuple[Node, Node, Node]]:
    doc_uri = f'{doc_name}'
    docN = ns[doc_uri]
    # (docN, ns.dengan_persetujuan, Literal(doc._dengan_persetujuan)),
    (docN, ns.menimbang, Literal(doc.menimbang)),
    triples: Triples = [
        # TODO: add raw text
        *point_content_to_triple(doc.menimbang, docN +
                                 '/menimbang', 'menimbang'),
        *point_content_to_triple(doc.mengingat, docN +
                                 '/mengingat', 'mengingat'),
        *itertools.chain(
            *[babs_to_triple(bab, docN) for bab in doc.babs]),
        (docN, RDF.type, ONS.Document),
        (docN, ONS.penjelasan, Literal(doc._name, datatype=XSD.string)),
        # (docN, ONS.pengesahan_text, Literal(
        #     doc.pengesahan_text, datatype=XSD.string)),
        # (docN, ONS.op_text, Literal(doc.op_text, datatype=XSD.string)),
        (docN, ONS.name, Literal(doc._name, datatype=XSD.string)),
        (docN, ONS.nomor, Literal(doc._nomor, datatype=XSD.integer)),
        (docN, ONS.tahun, Literal(doc._tahun, datatype=XSD.integer)),
        (docN, ONS.pemutus, Literal(doc._pemutus, datatype=XSD.string)),
        (docN, ONS.tentang, Literal(doc._tentang, datatype=XSD.string)),
        (docN, ONS.salinan, Literal(doc._salinan, datatype=XSD.string)),
        (docN, ONS.memutuskan, Literal(doc._memutuskan, datatype=XSD.string)),
        (docN, ONS.tempat_disahkan, Literal(
            doc._tempat_disahkan, datatype=XSD.string)),
        (docN, ONS.tanggal_disahkan, Literal(
            doc._tanggal_disahkan, datatype=XSD.string)),
        (docN, ONS.tempat_ditetapkan, Literal(
            doc._tempat_ditetapkan, datatype=XSD.string)),
        (docN, ONS.tanggal_ditetapkan, Literal(
            doc._tanggal_ditetapkan, datatype=XSD.string)),
        (docN, ONS.jabatan_pengesah, Literal(
            doc._jabatan_pengesah, datatype=XSD.string)),
        (docN, ONS.nama_pengesah, Literal(doc._nama_pengesah, datatype=XSD.string)),
        (docN, ONS.tempat_diundangkan, Literal(
            doc._tempat_diundangkan, datatype=XSD.string)),
        (docN, ONS.tanggal_diundangkan, Literal(
            doc._tanggal_diundangkan, datatype=XSD.string)),
        (docN, ONS.sekretaris, Literal(doc._sekretaris, datatype=XSD.string)),
        (docN, ONS.nama_dokumen, Literal(doc._dokumen, datatype=XSD.string)),
        *[
            (docN, ns.dengan_persetujuan, Literal(x)) for x in doc._dengan_persetujuan
        ]
    ]

    return triples
