from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, unset_jwt_cookies

from alexandria.modules.utils.util import get_current_user_jwt
from alexandria.modules.utils.vendor.flask_restplus_patched import Resource, Namespace
from alexandria.settings.extensions import api
from .serializers import *
from .utils import *

__author__ = 'oclay'

blueprint = Blueprint('user', __name__)

security_api = Namespace('Security', path='/')
api.add_namespace(security_api)


@security_api.route('/user/profile')
class UserDetailView(Resource):
    """
    Api endpoint to retrieve or update an user
    """

    @jwt_required
    @security_api.response(ProfileSchema())
    def get(self):
        return get_current_user_jwt()

    @security_api.response(ProfileSchema())
    @security_api.parameters(UpdateProfileSchema(), locations=('form',))
    def put(self, args):
        user = get_current_user_jwt()
        response = change_profile(args, user)
        return response


@security_api.route('/login')
class LoginView(Resource):
    """
    Api endpoint to login an user
    """

    @security_api.parameters(LoginSchema())
    def post(self, args):
        response = login_user(args)
        if not response['login']:
            return response, 401
        return response


@security_api.route('/logout')
class LogoutView(Resource):
    """
    Api endpoint to logout an authenticated user
    """

    @jwt_required
    def post(self):
        response = jsonify({'logout': True})
        unset_jwt_cookies(response)
        return response


@security_api.route('/registration')
class RegistrationView(Resource):
    """
    Api endpoint to sing up an user
    """

    @security_api.parameters(RegistrationSchema(), locations=('form', 'json'))
    def post(self, args):
        response = user_registration(args)
        return response


@security_api.route('/reset_password')
class ResetPassword(Resource):
    """
    Api endpoint to reset password
    """

    @security_api.parameters(EmailSchema())
    def post(self, args):
        response = send_reset_password_email(args['email'])
        if not response['send_mail']:
            return response, 401
        return response, 401


@security_api.route('/user/<int:id>/follow')
class FollowView(Resource):
    """
    Api endpoint for follow another users
    """

    @jwt_required
    def post(self, id):
        user = get_current_user_jwt()
        return follow_user(id, user)

    @jwt_required
    def delete(self, id):
        user = get_current_user_jwt()
        return unfollow_user(id, user)


@security_api.route('/user/followed')
class FollowedView(Resource):
    """
    Api endpoint for follow another users
    """

    @jwt_required
    def get(self):
        user = get_current_user_jwt()
        return users_followed_by(user)


@security_api.route('/contact-us')
class ContactView(Resource):
    """
    Api endpoint contact
    """

    def post(self, args):
        add_feedback(args)
        return {'message': 'Your message will be read by the team'}
