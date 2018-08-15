from flask import current_app as app, url_for, render_template, _request_ctx_stack
from flask_babel import gettext as _
from flask_jwt_extended import create_access_token,revoke_token
from flask_mail import Message
from flask_principal import Identity, RoleNeed, identity_changed
from flask_uploads import UploadNotAllowed

from alexandria.modules.utils.exceptions import FileSizeError, FileTypeError
from alexandria.modules.utils.util import token_generator
from alexandria.modules.utils.validators.files import validate_file_type, validate_file_size
from alexandria.settings.extensions import jwt, profile_image, mail, db
from authentication import authenticate
from models import User, PasswordRecovery, AccountRegistration, followers

__author__ = 'oclay'


@jwt.user_identity_loader
def user_identity_lookup(user):
    identity = Identity(user.username)
    if user.role:
        identity.provides.add(RoleNeed(user.role))
        identity_changed.send(app._get_current_object(), identity=identity)
    return user.username


@jwt.user_claims_loader
def add_claims_to_access_token(user):
    return {'role': user.role.code}


def login_user(args):
    user = authenticate(args['username'], args['password'])
    if user is None:
        return {'login': False, 'message': _('Bad username or password')}
    if not user.active:
        return {'login': False, 'message': _('Your account is pending for activation')}
    access_token = create_access_token(identity=user)
    return {'login': True, 'access_token': access_token}


def change_profile(args, user):
    try:
        if 'avatar' in args:
            validate_file_size(args['avatar'], app.config['MAX_IMAGE_SIZE'])
            validate_file_type(args['avatar'], 'image')
            avatar = profile_image.save(args['avatar'])
            args['avatar'] = avatar
        for arg in args:
            if args[arg]:
                setattr(user, arg, args[arg])
        db.session.commit()
        return {'profile_changed': True, 'message': _('Profile changed')}
    except (FileSizeError, FileTypeError) as ex:
        return {'profile_changed': False, 'message': ex.message}
    except UploadNotAllowed:
        return {'profile_changed': False, 'message': _('The image name has errors')}


def user_registration(args):
    del args['re_password']
    user = User(**args)
    db.session.add(user)
    db.session.commit()
    if app.config.get('SEND_REGISTRATION_MAIL', False):
        registration_message = send_registration_mail(args)
        return {'registration': True, 'message': registration_message}
    return {'registration': True, 'message': _('Wait for account activation')}


def send_registration_mail(user):
    try:
        subject = _("Email confirmation")
        generator = token_generator()
        token = generator.dumps(user.email, salt='email-confirm-key')
        confirm_url = url_for('activate', token=token, _external=True)
        html = render_template('email/activate.html', confirm_url=confirm_url)
        msg = Message(subject=subject, html=html)
        mail.send(msg)
        account_registration = AccountRegistration(token=token, user=user)
        db.session.add(account_registration)
        db.session.commit()
        return _("We send you an email, please check it.")
    except Exception as ex:
        return _("We have some problems with the mail server. Your account will be activated manually")


def send_reset_password_email(email):
    try:
        subject = _("Email confirmation")
        generator = token_generator()
        token = generator.dumps(email, salt='email-confirm-key')
        confirm_url = url_for('confirm_email', token=token, _external=True)
        html = render_template('email/password.html', confirm_url=confirm_url)
        msg = Message(subject=subject, html=html)
        mail.send(msg)
        return {'send_mail': True, 'message': _("We send you an email, please check out it.")}
    except Exception as ex:
        return {'send_mail': False, 'message': _("We have some problem with the mail server.")}


def active_user_by_token(args):
    account_registration = AccountRegistration.query.filter_by(token=args['token']).first()
    if account_registration:
        account_registration.user.active = True
        db.session.delete(account_registration)
        db.session.commit()
        return {'activate': True, 'message': _('Registration successful')}
    return {'activate': False}


def reset_password_by_token(args):
    """
    Reset password using a token
    """
    password_recovery = PasswordRecovery.query.filter_by(token=args['token']).first()
    if password_recovery:
        user = User.query.filter_byp(email=password_recovery.email).first()
        user.password = args['password']
        db.session.delete(password_recovery)
        db.session.commit()
        return {'password_reset': True}
    return {'password_reset': False}


def is_following(id, user):
    """
    Check if the user is already following by another
    :param id: User to know
    :param user: current user
    :return boolean
    """
    return user.followed.filter(followers.c.followed_id == id).count() > 0


def follow_user(id, user):
    """
    Follow a user
    :param id: user id to follow
    :param user: current user
    :return boolean
    """
    if not is_following(id, user):
        to_follow = User.query.filter_by(id=id).first()
        user.followed.append(to_follow)
        db.session.commit()
        return {'follow': True, 'message': _('Now you are following to this guy')}
    return {'follow': False, 'message': _('You are already following to this guy')}


def unfollow_user(id, user):
    """
    Follow a user
    :param id: user id to unfollow
    :param user: current user
    :return boolean
    """
    if is_following(id, user):
        to_unfollow = User.query.filter_by(id=id).first()
        user.followed.remove(to_unfollow)
        db.session.commit()
        return {'unfollow': True}
    return {'unfollow': False}


def users_followed_by(user):
    """
    Users that the current user is following 
    :param user: current user
    :return a list
    """
    return user.followed
