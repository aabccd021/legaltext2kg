import textract
text = textract.process('uu.pdf', method='pdfminer')

with open('textract.txt', 'w') as f:
    f.write(text)
