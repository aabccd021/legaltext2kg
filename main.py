# from typing import List
# import fitz
# import os
# import json
# import re
# import uuid

# from collections.abc import Mapping
# from rdflib import Literal, Graph, RDF, URIRef, BNode
# from rdflib.collection import Collection

# from text2dataclass.utils import extract_to_increment_key_list


# def extract_text(filename, pages):
#     content = [page.getText() for page in pages]
#     content = '\n'.join(content)
#     with open('extracted/{}.txt'.format(filename), 'w') as f:
#         f.write(content)
#     return content


# def split_element(lines):
#     content = {}
#     if lines[0].startswith('1.'):
#         for line in lines:
#             regex = r'^[0-9]*\.'
#             match = re.findall(regex, line)
#             if len(match) == 1:
#                 current_el_key = match[0]
#                 content[current_el_key] = []
#                 line = re.sub(regex, "", line)
#             elif len(match) > 1:
#                 raise Exception()
#             content[current_el_key].append(line)
#         return {'element': content}
#     return lines


# def split_ayat(lines):
#     lines = [line.strip() for line in lines]
#     if not lines[0].startswith('(1)'):
#         return lines
#     content = {}
#     for line in lines:
#         regex = r'^\([0-9]*\)'
#         match = re.findall(regex, line)
#         if len(match) == 1:
#             current_ayat_key = match[0]
#             content[current_ayat_key] = []
#             line = re.sub(regex, "", line)
#         elif len(match) > 1:
#             raise Exception()
#         content[current_ayat_key].append(line)
#     ayat_content = {}
#     for ayat_key in content.keys():
#         ayat_content[ayat_key] = split_element(content[ayat_key])
#     return {'ayat': ayat_content}


# def split_pasals(lines):
#     pasals = {}
#     for line in lines:
#         line = line.strip()
#         pasalNumberStr = line[6:]
#         if line.startswith("Pasal ") and represents_int(pasalNumberStr):
#             current_pasal_key = line
#             pasals[current_pasal_key] = []
#         else:
#             pasals[current_pasal_key].append(line)

#     final_pasals = {}
#     for pasal_key in pasals.keys():
#         final_pasals[pasal_key] = split_ayat(pasals[pasal_key])
#     return final_pasals


# def split_paragraph(lines):
#     if lines[0].startswith("Pasal "):
#         return split_pasals(lines)
#     if lines[0].startswith("Paragraf "):
#         content = dict()
#         judul = ""
#         for line in lines:
#             if line.startswith("Paragraf "):
#                 current_bagian_key = line
#                 content[current_bagian_key] = {'judul': '', 'isi': []}
#                 judul = ""
#             elif judul == "":
#                 judul = line
#                 content[current_bagian_key]['judul'] = judul
#             else:
#                 content[current_bagian_key]['isi'].append(line)
#         par_content = []
#         for bagian_key in content.keys():
#             content[bagian_key]['isi'] = split_pasals(
#                 content[bagian_key]['isi'])
#             par_content.append({
#                 'key': bagian_key,
#                 **content[bagian_key]
#             })
#         return {'paragraf': par_content}


# def split_bab_content(bab_lines):
#     if bab_lines[0].startswith("Pasal "):
#         return split_pasals(bab_lines)
#     if bab_lines[0].startswith("Bagian "):
#         content = dict()
#         judul = []
#         judulFinished = False
#         for line in bab_lines:
#             if line.startswith("Bagian "):
#                 current_bagian_key = line
#                 content[current_bagian_key] = {'judul': '', 'isi': []}
#                 judulFinished = False
#                 judul = []
#             elif not judulFinished:
#                 if line.startswith('Paragraf') or line.startswith('Pasal'):
#                     content[current_bagian_key]['judul'] = '\n'.join(judul)
#                     content[current_bagian_key]['isi'].append(line)
#                     judulFinished = True
#                 else:
#                     judul.append(line)
#             else:
#                 content[current_bagian_key]['isi'].append(line)

#         final_content = []
#         for bagian_key in content.keys():
#             content[bagian_key]['isi'] = split_paragraph(
#                 content[bagian_key]['isi'])

#             final_content.append({
#                 'key': bagian_key,
#                 **content[bagian_key]
#             })
#         return {'bagian': final_content}


# def represents_int(s):
#     try:
#         int(s)
#         return True
#     except ValueError:
#         return False


# def split_babs(content):
#     babs = dict()
#     last_bab = "PEMBUKAAN"
#     current_bab_content = ""
#     for line in content:
#         if line.startswith("BAB ") or line.startswith("P E N"):
#             babs[last_bab] = current_bab_content
#             current_bab_content = ""
#             last_bab = line
#         current_bab_content += line + "\n"
#     babs[last_bab] = current_bab_content

#     content = {
#         "metadata": "",
#         "bab": []
#     }
#     for key, val in babs.items():
#         if key == "PEMBUKAAN":
#             content["metadata"] = val
#         else:
#             val = val.splitlines()
#             judul = []
#             last_idx = 1
#             for title_idx in range(1, len(val)):
#                 v = val[title_idx]
#                 last_idx = title_idx
#                 if v == v.upper():
#                     judul.append(v)
#                 else:
#                     break
#             bab_content = {
#                 "key": key,
#                 "judul": "\n".join(judul),
#                 "isi": split_bab_content(val[last_idx:]),
#             }
#             content["bab"].append(bab_content)

#     return content


# def write_dict(filename, dictionary):
#     content = json.dumps(dictionary, indent=2)
#     with open('extracted/{}.json'.format(filename), 'w') as f:
#         f.write(content)


# def split_penjelasan(lines):
#     main = []
#     pengesahan = []
#     penjelasan = []
#     state = "main"
#     for line in lines:
#         if line.startswith("P E N J E L A S A N"):
#             state = "penjelasan"
#         elif line.startswith("Disahkan") or line.startswith("Ditetapkan"):
#             state = "pengesahan"

#         if state == "pengesahan":
#             pengesahan.append(line)
#         elif state == "penjelasan":
#             penjelasan.append(line)
#         else:
#             main.append(line)
#     print(len(lines))
#     print('isi', len(main))
#     print('penjelasan', len(penjelasan))
#     print('pengesahan', len(pengesahan))
#     print()
#     return main, pengesahan, penjelasan


# def preprocess(lines):
#     return [line.strip() for line in lines if line.strip() != ""]


# def addMetadata(g: Graph, data, fn):
#     b = BNode()
#     g.add((fn, u('hasMetadata'), b))
#     g.add((b, RDF.type, u('metadata')))
#     g.add((b, u('hasValue'), Literal(data['metadata'])))


# def generate_ayat(g: Graph, ayatKey, ayatValArrray):
#     b = BNode()
#     g.add((b, RDF.type, u('ayat')))
#     g.add((b, u('hasAyatNumber'), Literal(ayatKey)))
#     Collection(g, b, [Literal(x) for x in ayatValArrray])
#     return b


# def generate_ayats(g: Graph, ayat: dict):
#     b = BNode()
#     for ayatKey, ayatValArray in ayat.items():
#         ayat = generate_ayat(g, ayatKey, ayatValArray)
#         g.add((b, u('hasAyat'), ayat))
#     return b


# def generate_pasal(g: Graph, pasalNumber, pasalContents):
#     b = BNode()
#     g.add((b, RDF.type, u('pasal')))
#     g.add((b, u('hasPasalName'), Literal(pasalNumber)))
#     if isinstance(pasalContents, Mapping):
#         content = generate_ayats(g, pasalContents['ayat'])
#         g.add((b, u('hasPasalContent'), content))
#     else:
#         Collection(g, b, [Literal(x) for x in pasalContents])
#     return b


# def generate_isi_bab(g: Graph, isi):
#     b = BNode()
#     if set(isi.keys()) == {"bagian"}:
#         bagians = isi['bagian']
#         generatedBagians = [generate_bagian(g, bab) for bab in bagians]
#         Collection(g, b, generatedBagians)
#     elif set(isi.keys()) == {"paragraf"}:
#         return
#         # bagians = isi['paragraf']
#         # generatedBagians = [generate_(g, bab) for bab in bagians]
#     # if isi is pasal
#     else:
#         for key, value in isi.items():
#             g.add((b, u('hasPasal'), generate_pasal(g, key, value)))

#     return b


# def generate_bagian(g: Graph, bagian):
#     b = BNode()
#     g.add((b, RDF.type, u('bagian')))
#     g.add((b, u('hasKey'), Literal(bagian['key'])))
#     g.add((b, u('hasJudul'), Literal(bagian['judul'])))
#     isi = bagian['isi']
#     if set(isi.keys()) == {"paragraf"}:
#         None
#     else:
#         for key, value in isi.items():
#             g.add((b, u('hasPasal'), generate_pasal(g, key, value)))
#     return b


# def generateBab(g, bab):
#     b = BNode()
#     g.add((b, RDF.type, u('bab')))
#     g.add((b, u('hasKey'), Literal(bab['key'])))
#     g.add((b, u('hasJudul'), Literal(bab['judul'])))
#     g.add((b, u('hasIsi'), generate_isi_bab(g, bab['isi'])))
#     return b


# def addBab(g: Graph, data, fn):
#     b = BNode()
#     g.add((fn, u('hasBab'), b))
#     g.add((b, RDF.type, u('babs')))
#     babs = data['bab']
#     generatedBabs = [generateBab(g, bab) for bab in babs]
#     Collection(g, b, generatedBabs)
#     # g.add((mid, u('hasValue'), Literal(data['metadata'])))


# def u(string):
#     return URIRef('X:{}'.format(string))


# def process(filename):
#     pages = fitz.open('pdf/{}.pdf'.format(filename))
#     content = extract_text(filename, pages).splitlines()
#     content = preprocess(content)
#     main, _, __ = split_penjelasan(content)
#     structured = split_babs(main)
#     write_dict(filename, structured)
#     g = Graph()
#     fn = u(filename)
#     g.add((fn, RDF.type, u('Peraturan')))
#     addMetadata(g, structured, fn)
#     addBab(g, structured, fn)
#     g.serialize(
#         destination='extracted/{}.ttl'.format(filename),
#         format='turtle',
#     )


# if __name__ == "__main__":
#     for filename in ['UU13-2003', 'PERGUB33-2020']:
#         process(filename)
#     # raw_to_structured(g, content)
