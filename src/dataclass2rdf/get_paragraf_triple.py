import itertools
from typing import Iterable, cast
from rdflib.namespace import XSD
from rdflib.term import Literal, URIRef
from dataclass2rdf.get_pasal_triple import pasal_to_triple
from dataclass2rdf.types import Triples
from dataclass2rdf.utils import ONS
from text2dataclass.types import Bagian, BagianContent, Paragraf, Pasal


def paragraf_to_triple(
    paragraf: Paragraf,
    parent: URIRef,
    doc: URIRef,
) -> Triples:
    paragrafN = parent + f'/paragraf/{paragraf._key}'
    return [
        (parent, ONS.hasParagraf, paragrafN),
        (paragrafN, ONS.hasJudul, Literal(paragraf._judul, datatype=XSD.string)),
        (paragrafN, ONS.hasKey, Literal(paragraf._key, datatype=XSD.integer)),
        *itertools.chain(*[pasal_to_triple(p, paragrafN, doc) for p in paragraf.isi])
    ]
