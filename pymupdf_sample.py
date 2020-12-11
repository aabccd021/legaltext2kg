import fitz
pages = fitz.open('uu.pdf')
content = []
for page in pages:
    content.append(page.getText())
with open('pymupdf_text.txt', 'w') as f:
    f.write('\n'.join(content))
