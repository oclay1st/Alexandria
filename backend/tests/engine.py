# -*- coding: utf-8 -*-
# from unidecode import unidecode
from flask import current_app as app


def test_search_documenwts(client):
    params = {'criteria': 'microservices', 'page': 1}
    print app.engine.search_document(params)
    assert 1 == 1


def test_extrac_text_pdf(client):
    m = "365 días para ser m�s culto"
    import unicodedata
    aa = ['So', 'Cf', 'Cn', 'Cc']
    m = ''.join((c for c in unicodedata.normalize('NFD', unicode(m, 'utf-8')) if unicodedata.category(c) not in aa))
    assert 1 == 1


def test_index_docs():
    app.engine.index_document({'title': 'Python para todos', 'lang': 'es'})
    resp = app.engine.search_document({'title': 'python'})
    app.engine.delete_document(resp.id)


def test_search_docs():
    result = app.engine.search_document({'criteria': 'python', 'page': 1, 'per_page': 4})
    assert 1 == 1
