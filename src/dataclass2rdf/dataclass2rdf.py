# pyright: reportGeneralTypeIssues
from rdflib.namespace import NamespaceManager
from rdflib.term import Literal
from text2dataclass.types import LegalDocument
from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import XSD
from dataclass2rdf.utils import *


def dataclass2rdf(doc: LegalDocument, doc_name: str) -> Graph:
    g = Graph()
    docN = ns[doc_name]
    triples = [
        (docN, ns.penjelasan, Literal(doc._name, datatype=XSD.string)),
        (docN, ns.pengesahan_text, Literal(doc.pengesahan_text, datatype=XSD.string)),
        (docN, ns.op_text, Literal(doc.op_text, datatype=XSD.string)),
        # (docN, ns.babs, Literal(doc.babs)),
        (docN, ns.name, Literal(doc._name, datatype=XSD.string)),
        (docN, ns.nomor, Literal(doc._nomor, datatype=XSD.integer)),
        (docN, ns.tahun, Literal(doc._tahun, datatype=XSD.integer)),
        (docN, ns.pemutus, Literal(doc._pemutus, datatype=XSD.string)),
        # (docN, ns.dengan_persetujuan, Literal(doc._dengan_persetujuan)),
        (docN, ns.tentang, Literal(doc._tentang, datatype=XSD.string)),
        (docN, ns.salinan, Literal(doc._salinan, datatype=XSD.string)),
        (docN, ns.memutuskan, Literal(doc._memutuskan, datatype=XSD.string)),
        (docN, ns.tempat_disahkan, Literal(
            doc._tempat_disahkan, datatype=XSD.string)),
        (docN, ns.tanggal_disahkan, Literal(
            doc._tanggal_disahkan, datatype=XSD.string)),
        (docN, ns.tempat_ditetapkan, Literal(
            doc._tempat_ditetapkan, datatype=XSD.string)),
        (docN, ns.tanggal_ditetapkan, Literal(
            doc._tanggal_ditetapkan, datatype=XSD.string)),
        (docN, ns.jabatan_pengesah, Literal(
            doc._jabatan_pengesah, datatype=XSD.string)),
        (docN, ns.nama_pengesah, Literal(doc._nama_pengesah, datatype=XSD.string)),
        (docN, ns.tempat_diundangkan, Literal(
            doc._tempat_diundangkan, datatype=XSD.string)),
        (docN, ns.tanggal_diundangkan, Literal(
            doc._tanggal_diundangkan, datatype=XSD.string)),
        (docN, ns.sekretaris, Literal(doc._sekretaris, datatype=XSD.string)),
        (docN, ns.dokumen, Literal(doc._dokumen, datatype=XSD.string)),
        # (docN, ns.menimbang, Literal(doc.menimbang)),
        # (docN, ns.mengingat, Literal(doc.mengingat)),
    ]
    for triple in triples:
        g.add(triple)
    return g
