import fitz
import os
import json
import re
from rdflib import Literal, Graph


def extract_text(filename, pages):
    content = [page.getText() for page in pages]
    content = '\n'.join(content)
    with open('extracted/{}.txt'.format(filename), 'w') as f:
        f.write(content)
    return content


def raw_to_structured(g, content: str):
    g.add((Literal('a'), Literal('b'), Literal('c')))
    return


def split_element(lines):
    content = {}
    if lines[0].startswith('1.'):
        for line in lines:
            regex = r'^[0-9]*\.'
            match = re.findall(regex, line)
            if len(match) == 1:
                current_el_key = match[0]
                content[current_el_key] = []
                line = re.sub(regex, "", line)
            elif len(match) > 1:
                raise Exception()
            content[current_el_key].append(line)
        return {'element': content}
    return lines


def split_ayat(lines):
    lines = [line.strip() for line in lines]
    if not lines[0].startswith('(1)'):
        return lines
    content = {}
    for line in lines:
        regex = r'^\([0-9]*\)'
        match = re.findall(regex, line)
        if len(match) == 1:
            current_ayat_key = match[0]
            content[current_ayat_key] = []
            line = re.sub(regex, "", line)
        elif len(match) > 1:
            raise Exception()
        content[current_ayat_key].append(line)
    ayat_content = {}
    for ayat_key in content.keys():
        ayat_content[ayat_key] = split_element(content[ayat_key])
    return {'ayat': ayat_content}


def split_pasals(lines):
    pasals = {}
    for line in lines:
        line = line.strip()
        pasalNumberStr = line[6:]
        if line.startswith("Pasal ") and represents_int(pasalNumberStr):
            current_pasal_key = line
            pasals[current_pasal_key] = []
        else:
            pasals[current_pasal_key].append(line)

    final_pasals = {}
    for pasal_key in pasals.keys():
        final_pasals[pasal_key] = split_ayat(pasals[pasal_key])
    return final_pasals


def split_paragraph(lines):
    if lines[0].startswith("Pasal "):
        return split_pasals(lines)
    if lines[0].startswith("Paragraf "):
        content = dict()
        judul = ""
        for line in lines:
            if line.startswith("Paragraf "):
                current_bagian_key = line
                content[current_bagian_key] = {'judul': '', 'isi': []}
                judul = ""
            elif judul == "":
                judul = line
                content[current_bagian_key]['judul'] = judul
            else:
                content[current_bagian_key]['isi'].append(line)
        par_content = {}
        for par_idx, bagian_key in enumerate(content.keys()):
            content[bagian_key]['isi'] = split_pasals(
                content[bagian_key]['isi'])
            par_content[par_idx+1] = {
                'key': bagian_key,
                **content[bagian_key]
            }
        return {'paragraf': par_content}


def split_bab_content(bab_lines):
    if bab_lines[0].startswith("Pasal "):
        return split_pasals(bab_lines)
    if bab_lines[0].startswith("Bagian "):
        content = dict()
        judul = ""
        for line in bab_lines:
            if line.startswith("Bagian "):
                current_bagian_key = line
                content[current_bagian_key] = {'judul': '', 'isi': []}
                judul = ""
            elif judul == "":
                judul = line
                content[current_bagian_key]['judul'] = judul
            else:
                content[current_bagian_key]['isi'].append(line)
        final_content = {}
        for bagian_idx, bagian_key in enumerate(content.keys()):
            content[bagian_key]['isi'] = split_paragraph(
                content[bagian_key]['isi'])

            final_content[bagian_idx+1] = {
                'key': bagian_key,
                **content[bagian_key]
            }
        return {'bagian': final_content}


def represents_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def split_babs(content):
    babs = dict()
    last_bab = "PEMBUKAAN"
    current_bab_content = ""
    for line in content:
        if line.startswith("BAB ") or line.startswith("P E N"):
            babs[last_bab] = current_bab_content
            current_bab_content = ""
            last_bab = line
        current_bab_content += line + "\n"
    babs[last_bab] = current_bab_content

    content = {
        "metadata": "",
        "bab": {},
    }
    for idx, (key, val) in enumerate(babs.items()):
        if key == "PEMBUKAAN":
            content["metadata"] = val
        else:
            val = val.splitlines()
            judul = []
            last_idx = 1
            for title_idx in range(1, len(val)):
                v = val[title_idx]
                last_idx = title_idx
                if v == v.upper():
                    judul.append(v)
                else:
                    break
            bab_content = {
                "key": key,
                "judul": "\n".join(judul),
                "isi": split_bab_content(val[last_idx:]),
            }
            content["bab"][idx] = bab_content

    return content


def write_dict(filename, dictionary):
    content = json.dumps(dictionary, indent=2)
    with open('extracted/{}.json'.format(filename), 'w') as f:
        f.write(content)

# def remove_empty_line(lines):
    # return [ x for x if x.strip()]


def split_penjelasan(lines):
    main = []
    pengesahan = []
    penjelasan = []
    state = "main"
    for line in lines:
        if line.startswith("P E N J E L A S A N"):
            state = "penjelasan"
        elif line.startswith("Disahkan") or line.startswith("Ditetapkan"):
            state = "pengesahan"

        if state == "pengesahan":
            pengesahan.append(line)
        elif state == "penjelasan":
            penjelasan.append(line)
        else:
            main.append(line)
    return main, pengesahan, penjelasan


def preprocess(lines):
    return [line.strip() for line in lines if line.strip() != ""]


def process(filename):
    pages = fitz.open('{}.pdf'.format(filename))
    content = extract_text(filename, pages).splitlines()
    content = preprocess(content)
    main, pengesahan, penjelasan = split_penjelasan(content)
    structured = split_babs(main)
    write_dict(filename, structured)


if __name__ == "__main__":
    for filename in ['UU13-2003', 'PERGUB33-2020']:
        process(filename)
    # g = Graph()
    # raw_to_structured(g, content)
    # print(g.serialize(format="turtle").decode("utf-8"))
