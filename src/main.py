import json
import dataclasses
import os
from rdflib import Graph, graph

from rdflib.namespace import NamespaceManager
from dataclass2rdf.dataclass2rdf import dataclass2triples
from pdf2text.pdf2text import pdf2text
from text2dataclass.text2dataclass import text2dataclass
from dataclass2rdf.utils import ns, ONS


def get_graph(filename: str) -> Graph:
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
    return g


if __name__ == "__main__":
    filenames = ['UU13-2003', 'PERGUB33-2020']
    graphs = [get_graph(filename) for filename in filenames]
    # merge graphs
    g = graphs[0]
    if len(graphs) > 1:
        for gg in graphs[1:]:
            g += gg

    # query triple and write to file
    query_dir = "sample_queries"
    for q_file in os.listdir(query_dir):
        if q_file.endswith(".sparql"):
            # write file
            with open(f'{query_dir}/{q_file}') as f:
                qres = g.query('\n'.join(f.readlines()))
            vars = [v.toPython() for v in qres.vars]
            qres = '\n\n'.join(
                ['\n'.join([f'{v}: {x}' for x, v in zip(x, vars)]) for x in qres])
            q_filename = os.path.splitext(os.path.basename(q_file))[0]
            with open(f'{query_dir}/{q_filename}_result.txt', 'w') as f:
                f.write(qres)
