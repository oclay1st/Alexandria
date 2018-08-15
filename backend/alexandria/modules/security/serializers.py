from flask_babel import gettext as _
from marshmallow import fields, validate, validates_schema, ValidationError

from alexandria.modules.utils.api_helpers import not_blank, FileField, PasswordField
from alexandria.modules.utils.vendor.flask_restplus_patched import Parameters, Schema
from models import User

__author__ = 'oclay'

not_min_8 = validate.Length(
    min=8, error=_('Field cannot have lower than %(num)s characters', num=8))
not_min_5 = validate.Length(
    min=5, error=_('Field cannot have lower than %(num)s characters', num=5))


def validate_user_exist(username):
    if User.query.filter_by(username=username).first():
        raise ValidationError(_("This username is already taken"), ['username'])


class ProfileSchema(Schema):
    username = fields.String()
    name = fields.String()
    email = fields.Email()
    avatar_url = fields.String()


class LoginSchema(Parameters):
    username = fields.String(
        validate=not_blank,
        required=True,
        error_messages={'required': _('This filed is required')}
    )
    password = PasswordField(
        validate=not_blank,
        required=True,
        error_messages={'required': _('This filed is required')}
    )

    class Meta:
        strict = True


class EmailSchema(Parameters):
    email = fields.Email(
        required=True,
        error_messages={'required': _('This filed is required')})

    class Meta:
        strict = True


class UserSchema(Parameters):
    username = fields.String(validate=[validate_user_exist, not_min_5])
    name = fields.String(validate=not_min_5)
    email = fields.Email()
    password = fields.String(validate=not_min_8)
    re_password = fields.String()


class RegistrationSchema(UserSchema):
    def __init__(self, **agrs):
        super(self.__class__, self).__init__(**agrs)
        for key in self.fields:
            self.fields[key].required = True

    class Meta:
        strict = True

    @validates_schema(pass_original=True)
    def validate_fields(self, data, original):
        fields_errors = [field for field in self.fields.keys() if field not in original]
        if fields_errors:
            raise ValidationError(_('This filed is required'), fields_errors)


class UpdateProfileSchema(UserSchema):
    current_password = fields.String()
    avatar = FileField(location='files')

    def __init__(self, **agrs):
        super(self.__class__, self).__init__(**agrs)
        del (self.fields['username'])

    class Meta:
        strict = True

    @validates_schema(pass_original=True)
    def validate_fields(self, data, original):
        """Validate the data"""

        if not original.viewkeys() & self.fields.keys():  # :check almost one is present
            raise ValidationError(
                'Almost one element:%s' % self.fields.keys(), ['error'])

        password_keys = ['current_password', 'password', 're_password']
        if original.viewkeys() & password_keys:  # :if one is present ,the others must be too
            fields_errors = [
                key for key in password_keys if key not in original]
            required_message = _('This filed is required')
            raise ValidationError(required_message, fields_errors)

        elif 'password' in data and data['password'] != data['re_password']:
            raise ValidationError(_('Password missmatch'), ['re_password'])
