from rdflib.namespace import XSD
from rdflib.term import Literal, URIRef
from dataclass2rdf.get_strs_or_points_triple import point_content_to_triple
from text2dataclass.types import Ayat, Pasal
from dataclass2rdf.types import Triples
from dataclass2rdf.utils import ONS


def ayat_to_triple(
    ayat: Ayat,
    parent: URIRef,
) -> Triples:
    ayatN = parent + f'/ayat/{ayat._key}'
    return [
        (parent, ONS.hasAyat, ayatN),
        (ayatN, ONS.hasKey, Literal(ayat._key, datatype=XSD.integer)),
        *point_content_to_triple(ayat.isi, ayatN, "hasContent")
    ]
