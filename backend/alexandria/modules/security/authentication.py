from flask import current_app as app

from models import User

__author__ = 'oclay'


class LDAPBackend(object):
    """ldap authentication class"""

    @staticmethod
    def authenticate(username, password):
        return NotImplementedError


class ClassicBackend(object):
    """classic authentication class"""

    @staticmethod
    def authenticate(username, password):
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            return user
        return None


def authenticate(username, password):
    if 'AUTH_BACKEND' not in app.config:
        raise Exception("Improperly configured: AUTH_BACKEND missing")
    if app.config['AUTH_BACKEND'] == 'LDAP':
        return LDAPBackend.authenticate(username, password)
    if app.config['AUTH_BACKEND'] == 'Classic':
        return ClassicBackend.authenticate(username, password)
