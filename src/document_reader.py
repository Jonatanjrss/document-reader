import re
import unicodedata
import mimetypes
from pathlib import Path
from typing import List

import pdftotext
from loguru import logger


class PDFReader:
    def __init__(self, filename):
        self.filename = filename

        with open(filename, "rb") as fp:
            self._pages = pdftotext.PDF(fp)

    def extract(self, fields: List):
        found = []

        for field in fields:
            mo = re.search(field.regex, clean(self._pages[field.page]))
            if mo:
                found.append({field.name: mo.group()})
        return found


class Field:
    def __init__(self, name, regex, page=None):
        if not page:
            page = 0
        else:
            page = page - 1
        self.name = name
        self.regex = regex
        self.page = page


class Document:
    r"""Usage:

    >>> from document_reader import Document, Field
    >>> doc = Document("pdf_file.pdf")
    >>> doc.register_fields(
        Field(name="contract", regex=r"\d+/.*?/\d+", page=0),
        Field(name="nup", regex=r"\d{5}\.\d{6}/\d{4}-\d{2}", page=1),
    )
    >>> data = doc.open()
    >>> print(data)"""

    fields = []
    pdf_reader = PDFReader

    def register_fields(self, *fields):
        for field in fields:
            self.fields.append(field)

    def __init__(self, filename: str|Path):
        self.filename = Path(filename)

    def open(self):
        mime_type = mimetypes.guess_type(self.filename)[0]
        logger.debug(f'Abrindo arquivo do tipo {mime_type}')
        content = None
        match mime_type:
            case "application/pdf":
                content = self.open_pdf_file()
        return content

    def open_pdf_file(self):
        return self.pdf_reader(self.filename).extract(self.fields)


def clean(string):
    string = unicodedata.normalize('NFKC', string)
    string = string.replace('\n', ' ')
    while '  ' in string:
        string = string.replace('  ', ' ')
    string = string.replace(" ,", ",")
    return string