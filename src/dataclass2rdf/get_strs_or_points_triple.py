from typing import Iterable, List, Tuple, cast
from rdflib.namespace import RDF, XSD
from rdflib.term import Node, URIRef, Literal
from dataclass2rdf.types import Triples
from text2dataclass.types import Point, Points, StrsOrPoints
from dataclass2rdf.utils import *
import itertools


def point_content_to_triple(
    p: StrsOrPoints,
    parent: URIRef,
    rel: str,
) -> Triples:
    if type(p) == str:
        return [(parent, ONS[rel], Literal(cast(str, p), datatype=XSD.string))]
    if type(p) == Iterable[str]:
        return [(parent, ONS[rel], Literal(x, datatype=XSD.string)) for x in cast(Iterable[str], p)]
    if type(p) == Points:
        points = cast(Points, p)
        return [
            (parent, ONS.description, Literal(
                points._description, datatype=XSD.string)),
            # (pointsN, ONS.text, Literal(points.text, datatype=XSD.string)),
            *itertools.chain(
                *[point_to_triple(isi, parent) for isi in points.isi])
        ]
    raise Exception()


def point_to_triple(
    p: Point,
    parent: URIRef,
) -> Triples:
    pointN = parent + f'/point/{p._key}'
    datatype = XSD.string if type(p._key) == str else XSD.integer
    return [
        (pointN, PartOf, parent),
        (pointN, RDF.type, ONS.Point),
        (pointN, ONS.hasKey, Literal(p._key, datatype=datatype)),
        *point_content_to_triple(p.isi, pointN, "hasContent")
    ]
