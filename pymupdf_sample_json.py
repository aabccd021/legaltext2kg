import fitz
pages = fitz.open('uu.pdf')
for i, page in enumerate(pages):
    with open('pymupdf_json/{}.json'.format(i), 'w') as f:
        f.write(page.getText('json'))
