import itertools
from typing import Iterable, cast
from rdflib.namespace import RDF, XSD
from rdflib.term import Literal, URIRef
from dataclass2rdf.get_paragraf_triple import paragraf_to_triple
from dataclass2rdf.get_pasal_triple import pasal_to_triple
from dataclass2rdf.types import Triples
from dataclass2rdf.utils import ONS, PartOf
from text2dataclass.types import Bagian, BagianContent, Paragraf, Pasal


def bagian_to_triple(
    bagian: Bagian,
    parent: URIRef,
    doc: URIRef,
) -> Triples:
    bagianN = parent + f'/bagian/{bagian._key}'
    return [
        (bagianN, PartOf, parent),
        (bagianN, ONS.hasJudul, Literal(bagian._judul, datatype=XSD.string)),
        (bagianN, ONS.hasKey, Literal(bagian._key, datatype=XSD.integer)),
        (bagianN, RDF.type, ONS.Bagian),
        *bagian_content_to_triple(bagian.isi, bagianN, doc)
    ]


def bagian_content_to_triple(
    c: BagianContent,
    parent: URIRef,
    doc: URIRef,
) -> Triples:
    c = list(cast(Iterable, c))
    if type(c[0]) == Pasal:
        c = cast(Iterable[Pasal], c)
        return list(itertools.chain(*[pasal_to_triple(x, parent, doc) for x in c]))
    elif type(c[0]) == Paragraf:
        c = cast(Iterable[Paragraf], c)
        return list(itertools.chain(*[paragraf_to_triple(x, parent, doc) for x in c]))
    raise Exception()
