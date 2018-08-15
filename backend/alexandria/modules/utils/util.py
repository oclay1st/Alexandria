from flask import current_app as app
from flask_jwt_extended import get_jwt_identity
from flask_principal import Permission, RoleNeed
from flask_restplus.errors import abort
from itsdangerous import URLSafeTimedSerializer

from alexandria.modules.security.models import User

__author_ = 'oclay'


def token_generator():
    return URLSafeTimedSerializer(app.config["SECRET_KEY"])


admin_permission = Permission(RoleNeed('Admin'))


def get_current_user_jwt():
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()
    if not user:
        abort(code=404, message="User no found")
    return user
