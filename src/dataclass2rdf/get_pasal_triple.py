
from typing import Iterable, cast
from rdflib.namespace import XSD, RDF
from rdflib.term import Literal, URIRef
from dataclass2rdf.get_ayat_triple import ayat_to_triple
from dataclass2rdf.get_strs_or_points_triple import point_content_to_triple

from dataclass2rdf.types import Triples
from dataclass2rdf.utils import ONS, PartOf
from text2dataclass.types import Ayat, Pasal, PasalContent, Points, StrsOrPoints
import itertools


def pasal_to_triple(
    pasal: Pasal,
    parent: URIRef,
    doc: URIRef,
) -> Triples:
    pasalN = doc + f'/pasal/{pasal._key}'
    return [
        (pasalN, PartOf, parent),
        (pasalN, ONS.hasKey, Literal(pasal._key, datatype=XSD.integer)),
        (pasalN, RDF.type, ONS.Pasal),
        *pasal_content_to_triple(pasal.isi, pasalN)
    ]


def pasal_content_to_triple(
    c: PasalContent,
    parent: URIRef,
) -> Triples:
    if type(c) in [Iterable[str], Points, str]:
        return point_content_to_triple(cast(StrsOrPoints, c), parent, "hasContent")
    c = list(cast(Iterable[Ayat], c))
    return list(itertools.chain(*[ayat_to_triple(a, parent) for a in c]))
