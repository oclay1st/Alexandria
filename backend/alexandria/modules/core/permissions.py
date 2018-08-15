from flask_principal import Permission, RoleNeed

from alexandria.modules.utils.util import get_current_user_jwt

__author__ = 'oclay'


def is_document_owner(document):
    return document.user == get_current_user_jwt()

is_moderator = Permission(RoleNeed('moderator'))

is_contributor = Permission(RoleNeed('contributor'))


