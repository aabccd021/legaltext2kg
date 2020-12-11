import io
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams


def to_txt(pdf_path):
    input_ = file('uu.pdf', 'rb')
    output = io.StringIO()

    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    process_pdf(manager, converter, input_)

    return output.getvalue()
