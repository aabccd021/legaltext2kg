from typing import List
import fitz


def pdf2text(filename: str) -> List[str]:
    pages = fitz.Document('pdf/{}.pdf'.format(filename))
    page_contents: List[str] = [page.getText() for page in pages]
    processed_content = ['\n'.join(line.strip().splitlines())
                         for line in page_contents]
    file_content: str = '\n'.join(processed_content)
    with open('extracted/{}.txt'.format(filename), 'w') as f:
        f.write(file_content)
    return [x.strip() for x in file_content.splitlines()]
