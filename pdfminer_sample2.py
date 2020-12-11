from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import (
    LAParams,
    LTContainer,
    LTTextLine,
)
import json


def get_objs(layout, results):
    if not isinstance(layout, LTContainer):
        return
    for obj in layout:
        if isinstance(obj, LTTextLine):
            results.append(
                {'bbox': obj.bbox, 'text': obj.get_text(), 'type': type(obj)})
        get_objs(obj, results)


def get_text(path):
    a = []
    with open(path, "rb") as f:
        parser = PDFParser(f)
        document = PDFDocument(parser)
        if not document.is_extractable:
            raise PDFTextExtractionNotAllowed
        # https://pdfminersix.readthedocs.io/en/latest/api/composable.html#
        laparams = LAParams(
            all_texts=True,
        )
        rsrcmgr = PDFResourceManager()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(document):
            interpreter.process_page(page)
            layout = device.get_result()
            results = []
            a.append('objs-------------------------')
            get_objs(layout, results)
            for r in results:
                a.append(str(r))
    return '\n'.join(a)


p = get_text('uu.pdf')
with open('pdfminer2.txt', 'w') as f:
    f.write(p)
