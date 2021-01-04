from pdf2text.pdf2text import pdf2text
import json
import dataclasses

from text2json.text2json import text2json


def process(filename: str) -> None:
    text = pdf2text(filename)
    jsonFile = text2json(text)
    a = dataclasses.asdict(jsonFile)
    with open(f'extracted/{filename}.json', 'w') as f:
        f.write(json.dumps(a, indent=2, sort_keys=True))
        # f.write(str(jsonFile.babs[0]))
    # main, _, _ = split_penjelasan(content)
    # structured = split_babs(main)
    # write_dict(filename, structured)
    # g = Graph()
    # fn = u(filename)
    # g.add((fn, RDF.type, u('Peraturan')))
    # addMetadata(g, structured, fn)
    # addBab(g, structured, fn)
    # g.serialize(
    #     destination='extracted/{}.ttl'.format(filename),
    #     format='turtle',
    # )


if __name__ == "__main__":
    for filename in [
        'UU13-2003',
        'PERGUB33-2020'
    ]:
        process(filename)
