import PyPDF2
from PyPDF2.pdf import ContentStream

with open("uu.pdf", "rb") as fp:
    pdf = PyPDF2.PdfFileReader(fp)
    for page_no in range(pdf.numPages):
        if (page_no < 2):
            page = pdf.getPage(page_no)
            content = page['/Contents'].getObject()
            if not isinstance(content, ContentStream):
                content = ContentStream(content, pdf)
            for operands, operator in content.operations:
                print(operands, operator)
