import os

from flask import current_app as app
import pytest
from alexandria.modules.utils.parsers.parser import PDFParser


@pytest.fixture(params=['AngularJS_Novice_to_Ninja.pdf'])
def pdf(request, resources_path):
    return PDFParser(os.path.join(resources_path, request.param), app.config['MAX_PAGES'])


def test_pdf_text(pdf):
    pdf.pdf_lines_to_text()


def test_read_metadata(pdf):
    pdf.read_metadata()


def test_generate_thumbnail(client, pdf, resources_path):
    path = os.path.join(resources_path, pdf.name + '.png')
    pdf.generate_thumbnail(path, 180, 220)
    assert os.path.exists(path)
