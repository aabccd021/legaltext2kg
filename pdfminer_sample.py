from pdfminer.high_level import extract_text
content = extract_text('uu.pdf')

with open('pdf_miner.txt', mode='w') as f:
  f.write(content)