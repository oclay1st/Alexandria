from flask_babel import gettext as _
from marshmallow import fields, validate

from vendor.flask_restplus_patched import Parameters

__author__ = 'oclay'


class TokenSchema(Parameters):
    Authorization = fields.Integer(
        required=True,
        location='headers',
        error_messages={'required': _('This field is required')}
    )

    class Meta:
        strict = True


not_blank = validate.Length(min=1, error=_('Field cannot be blank'))


class FileField(fields.Field):
    def __init__(self, **agrs):
        super(self.__class__, self).__init__(**agrs)
        setattr(self, '__swagger_field_mapping', ('file', None))  # wire


class PasswordField(fields.String):
    def __init__(self, **agrs):
        super(self.__class__, self).__init__(**agrs)
        setattr(self, '__swagger_field_mapping', ('string', 'password'))  # wire
