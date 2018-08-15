import os

try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin
from datetime import datetime
from flask import request
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_utils.types.choice import ChoiceType
from flask_babel import gettext as _
from alexandria.settings.extensions import profile_image
from alexandria.settings.extensions import db


__author__ = 'oclay'


user_favorite_documents = db.Table('user_favorite_document',
                                   db.Column('document_id', db.Integer,
                                             db.ForeignKey('document.id', ondelete="CASCADE")),
                                   db.Column('user_id', db.Integer, db.ForeignKey('user.id')))

followers = db.Table('followers',
                     db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('followed_id', db.Integer, db.ForeignKey('user.id')))


class User(db.Model):
    """
    Class reference to user
    """
    ROLES = [(u'admin', _('Admin')), (u'contributor', _('Contributor')), (u'moderator', _('Moderator'))]

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    _password = db.Column(db.String(255))
    email = db.Column(db.String(120), unique=True)
    name = db.Column(db.String(120))
    joined_date = db.Column(db.DateTime, default=datetime.now())
    active = db.Column(db.Boolean, default=False)
    _avatar = db.Column(db.String(100), default='default.png')
    role = db.Column(ChoiceType(ROLES), default=u'')

    #: Relationships with others models
    documents = db.relationship('Document', backref='user', lazy='dynamic')
    account_registration = db.relationship('AccountRegistration', backref='user', lazy='dynamic')
    favorite_documents = db.relationship('Document', secondary=user_favorite_documents,
                                         backref=db.backref('users', lazy='dynamic'), lazy='dynamic')

    followed = db.relationship('User', secondary=followers, primaryjoin=(followers.c.follower_id == id),
                               secondaryjoin=(followers.c.followed_id == id),
                               backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def __getitem__(self, item):
        return getattr(self, item, None)

    @property
    def avatar_file(self):
        return profile_image.path(self.avatar)

    @property
    def avatar_url(self):
        if not os.path.exists(profile_image.path(self.avatar)):
            return urljoin(request.url_root, profile_image.url(self.username + '/default.png'))
        return urljoin(request.url_root, profile_image.url(self.username + '/' + self.avatar))

    @hybrid_property
    def avatar(self):
        return self._avatar

    @avatar.setter
    def avatar(self, avatar):
        if self._avatar != 'default.png':
            os.remove(self.avatar_file)
        self._avatar = avatar

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, plaintext_password):
        self._password = generate_password_hash(plaintext_password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class PasswordRecovery(db.Model):
    """
    Class reference to the password recovery impl
    """

    __tablename__ = 'password_recovery'

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(255))
    email = db.Column(db.String(255))


class AccountRegistration(db.Model):
    """
    Class reference to the account registration
    """

    __tablename__ = 'account_registration'

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
