from datetime import datetime

try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin

from flask import request

from sqlalchemy_utils.types.choice import ChoiceType
from flask_babel import gettext as _
from alexandria.settings.extensions import db, document_file, thumbnail_image

__author__ = 'oclay'

tags = db.Table('document_tag',
                db.Column('document_id', db.Integer, db.ForeignKey('document.id')),
                db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')))

DOCUMENT_STATUS = [(u'pending', _('Pending')), (u'approved', _('Approved'))]


class Document(db.Model):
    """
    Class reference to documents
    """

    __tablename__ = "document"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    author = db.Column(db.String(255))
    lang = db.Column(db.String(2))
    filename = db.Column(db.String(255), nullable=False)
    size = db.Column(db.Integer)
    pages = db.Column(db.Integer)
    thumbnail = db.Column(db.String(100), default='default.png')
    creation_date = db.Column(db.DateTime)
    upload_date = db.Column(db.DateTime, default=datetime.now())
    likes = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    status = db.Column(ChoiceType(DOCUMENT_STATUS), default=u'')

    #: Relationships with others models
    tags = db.relationship('Tag', secondary=tags, backref=db.backref('documents', lazy='dynamic'))

    def __getitem__(self, item):
        return getattr(self, item, None)

    @property
    def file(self):
        return document_file.path(self.filename)

    @property
    def file_url(self):
        return urljoin(request.url_root, document_file.url(self.filename))

    @property
    def thumbnail_url(self):
        return urljoin(request.url_root, thumbnail_image.url(self.thumbnail))


class Tag(db.Model):
    """
    Class reference to document's tags 
    """

    __tablename__ = "tag"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

    def __str__(self):
        return self.name
