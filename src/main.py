import json
import dataclasses
import os
from rdflib import Graph

from rdflib.namespace import NamespaceManager
from dataclass2rdf.dataclass2rdf import dataclass2triples
from pdf2text.pdf2text import pdf2text
from text2dataclass.text2dataclass import text2dataclass
from dataclass2rdf.utils import ns, ONS


def process(filename: str) -> None:
    # pdf2text
    text = pdf2text(filename)
    with open('extracted/{}.txt'.format(filename), 'w') as f:
        f.write("\n".join(text))

    # text2data
    data = text2dataclass(text)
    with open(f'extracted/{filename}.json', 'w') as f:
        f.write(json.dumps(dataclasses.asdict(data), indent=2, sort_keys=True))

    # data2triple
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

    # query
    query_dir = "sample_queries"
    for q_file in os.listdir(query_dir):
        if q_file.endswith(".sparql"):
            # make dir
            dir_path = f'{query_dir}/{filename}'
            os.makedirs(dir_path, exist_ok=True)
            # write file
            with open(f'{query_dir}/{q_file}') as f:
                qres = g.query('\n'.join(f.readlines()))
            qres = "\n\n".join(['{}\n{}\n{}'.format(*x) for x in qres])
            q_filename = os.path.splitext(os.path.basename(q_file))[0]
            with open(f'{dir_path}/{q_filename}.txt', 'w') as f:
                f.write(qres)


if __name__ == "__main__":
    for filename in ['UU13-2003', 'PERGUB33-2020']:
        process(filename)
