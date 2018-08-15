from flask import current_app as app
from alexandria.modules.core.utils import add_to_favorites, remove_from_favorites
from alexandria.settings.extensions import db
from alexandria.modules.core.models import Document
from alexandria.modules.security.models import User


def test_favorites(client,user_test):
    doc1 = Document.query.filter_by(title='Fluent Python').first()
    add_to_favorites(doc1.id, user_test)
    assert test.favorite_documents.count() == 1
    remove_from_favorites(doc1.id, test)
    assert test.favorite_documents.count() == 0
