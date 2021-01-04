from typing import Iterable, List, Tuple, cast
from rdflib.namespace import RDF, XSD
from rdflib.term import Node, URIRef, Literal
from dataclass2rdf.get_bagian_triple import bagian_to_triple
from dataclass2rdf.get_pasal_triple import pasal_to_triple
from dataclass2rdf.types import Triples
from text2dataclass.types import Bab, BabContent, Bagian, Pasal, Point, Points, StrsOrPoints
from dataclass2rdf.utils import *
import itertools


def babs_to_triple(
    bab: Bab,
    doc: URIRef,
) -> Triples:
    babN = doc + f'/bab/{bab._key}'
    return [
        (doc, ONS.hasBab, babN),
        (babN, ONS.hasJudul, Literal(bab._judul, datatype=XSD.string)),
        (babN, ONS.hasKey, Literal(bab._key, datatype=XSD.integer)),
        *bab_content_to_triple(bab.isi, babN, doc)
    ]


def bab_content_to_triple(
    c: BabContent,
    parent: URIRef,
    doc: URIRef,
) -> Triples:
    c = list(cast(Iterable, c))
    if type(c[0]) == Pasal:
        c = cast(Iterable[Pasal], c)
        return list(itertools.chain(*[pasal_to_triple(x, parent, doc) for x in c]))
    elif type(c[0]) == Bagian:
        c = cast(Iterable[Bagian], c)
        return list(itertools.chain(*[bagian_to_triple(x, parent, doc) for x in c]))
    raise Exception()
