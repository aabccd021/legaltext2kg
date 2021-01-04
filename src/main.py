import json
import dataclasses

from rdflib.namespace import NamespaceManager
from dataclass2rdf.dataclass2rdf import dataclass2rdf
from pdf2text.pdf2text import pdf2text
from text2dataclass.text2dataclass import text2dataclass
from dataclass2rdf.utils import ns


def process(filename: str) -> None:
    text = pdf2text(filename)

    with open('extracted/{}.txt'.format(filename), 'w') as f:
        f.write("\n".join(text))

    data = text2dataclass(text)

    with open(f'extracted/{filename}.json', 'w') as f:
        f.write(json.dumps(dataclasses.asdict(data), indent=2, sort_keys=True))

    rdf = dataclass2rdf(data, filename)
    nsm = NamespaceManager(rdf)
    nsm.bind('', ns)
    rdf.serialize(
        destination='extracted/{}.ttl'.format(filename),
        format='turtle',
        nsm=nsm
    )


if __name__ == "__main__":
    for filename in [
        'UU13-2003',
        'PERGUB33-2020'
    ]:
        process(filename)
