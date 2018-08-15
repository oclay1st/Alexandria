# -*- coding: utf-8 -*-
import os
from datetime import datetime
from time import mktime, strptime

from langdetect import detect

from pdf import poppler as pdf_document

__author__ = 'oclay'


class Parser(object):
    """ Parser document type"""

    def __init__(self, path, max_pages):
        self.path = path
        self.max_pages = max_pages

    def read_metadata(self):
        raise NotImplementedError

    def generate_thumbnail(self, *args):
        raise NotImplementedError

    def get_formated_date(self, date):
        date_string = date[2:16]  # example -- D:20160106140500+05'30'
        extract_format = strptime(date_string, "%Y%m%d%H%M%S")
        format_date = datetime.fromtimestamp(mktime(extract_format))
        return format_date


class PDFParser(Parser):
    """ Parser for pdf files ,extract metadata """

    def __init__(self, path, max_pages):
        Parser.__init__(self, path, max_pages)
        self.name = self.path.split(os.sep)[-1][:-4]  # :without extension
        self.parser = pdf_document.Document(self.path, self.max_pages)

    def pdf_lines_to_text(self):
        """
        devuelve el texto del pdf optimizando linea por linea y aun con la
        complejidad del metodo las classes estan creadas mediantes
        iteradores y escrito en cython lo cual permite generar
        un tiempo de respuesta muy cercano a la version en C/C++.
        """
        lines = [line.text.encode('utf-8')
                 for pages in self.parser
                 for flows in pages
                 for blocks in flows
                 for line in blocks]
        return ''.join(lines)

    def pdf_original_to_text(self, pages=None):
        """
        devuelve el texto del pdf manteniendo la estructura
        original del mismo con mucha eficiencia.
        """
        return self.parser.get_text(pages)

    def get_language(self):
        content = self.parser.get_text(5)
        return detect(unicode(content, 'utf-8'))

    def read_metadata(self):
        meta = self.parser.get_metadata()
        metadata = {'Title': u'', 'Author': u'', 'CreationDate': None}
        for key in metadata:
            if key in meta:
                metadata[key] = meta[key]
        metadata['NumPages'] = self.parser.num_pages
        metadata['Content'] = self.pdf_lines_to_text()
        metadata['Lang'] = self.get_language()
        metadata['CreationDate'] = self.get_formated_date(metadata['CreationDate'])

        return metadata

    def generate_thumbnail(self, path, x_scale_to, y_scale_to, img_format='png', page=1):
        self.parser.generate_thumbnail(path, x_scale_to, y_scale_to, img_format, page)

    def get_text_ocr(self):
        if self.parser.is_ok():
            pass

    def apply_ocr_to_pdf(self):
        raise NotImplementedError

