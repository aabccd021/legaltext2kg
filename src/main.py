import json
import dataclasses
from rdflib import Graph

from rdflib.namespace import NamespaceManager
from dataclass2rdf.dataclass2rdf import dataclass2triples
from pdf2text.pdf2text import pdf2text
from text2dataclass.text2dataclass import text2dataclass
from dataclass2rdf.utils import ns, ONS


def process(filename: str) -> None:
    text = pdf2text(filename)

    with open('extracted/{}.txt'.format(filename), 'w') as f:
        f.write("\n".join(text))

    data = text2dataclass(text)

    with open(f'extracted/{filename}.json', 'w') as f:
        f.write(json.dumps(dataclasses.asdict(data), indent=2, sort_keys=True))

    triples = dataclass2triples(data, filename)
    g = Graph()
    for triple in triples:
        g.add(triple)
    g.bind('', ns)
    g.bind('legal', ONS)
    g.serialize(
        destination='extracted/{}.ttl'.format(filename),
        format='turtle',
    )


if __name__ == "__main__":
    for filename in [
        'UU13-2003',
        'PERGUB33-2020'
    ]:
        process(filename)
