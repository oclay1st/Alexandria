from datetime import datetime

from flask_babel import gettext as _
from humanize import naturalsize, naturaltime
from marshmallow import fields, ValidationError, validate, validates_schema

from alexandria.modules.utils.api_helpers import FileField
from alexandria.modules.utils.api_helpers import not_blank
from alexandria.modules.utils.vendor.flask_restplus_patched import Parameters, Schema

__author__ = 'oclay'


class UploadSchema(Parameters):
    document = FileField(
        required=True,
        location='files',
        error_messages={'required': _('This field is required')})

    class Meta:
        strict = True


class UpdateSchema(Parameters):
    title = fields.String(validate=not_blank)
    author = fields.String(validate=not_blank)
    tags = fields.String()

    class Meta:
        strict = True
        partial = True

    @validates_schema(pass_original=True)
    def validate_fields(self, data, original):
        if not original.viewkeys() & {'title', 'author', 'tags'}:
            raise ValidationError(_('Almost one field: author,tags or title'),
                                  ['error'])


class PageSchema(Parameters):
    page = fields.Integer(missing=1)

    class Meta:
        strict = True


class SearchBaseSchema(Parameters):
    criteria = fields.String(
        required=True,
        error_messages={'required': _('This param is required')}
    )

    class Meta:
        strict = True


class SearchSchema(SearchBaseSchema, PageSchema):
    author = fields.String()
    tags = fields.String()
    per_page = fields.Int(
        missing=10,
        validate=validate.Range(
            min=1, max=10, error=_('Field must be between 1 and 10')))
    lang = fields.String()
    creation_date = fields.String()

    class Meta:
        strict = True


class DocumentSchema(Schema):
    url = fields.Function(lambda obj: ('/document/' + str(obj.id)))
    title = fields.String()
    author = fields.String()
    file_url = fields.String()
    thumbnail_url = fields.String()
    pages = fields.Integer()
    upload_date = fields.Function(lambda obj: naturaltime(datetime.now() - obj.upload_date))
    creation_date = fields.DateTime()
    likes = fields.Integer()
    size = fields.Function(lambda obj: naturalsize(obj.size))


class DocumentPaginationSchema(Schema):
    page = fields.Integer()
    pages = fields.Integer()
    total = fields.Integer()
    documents = fields.List(attribute='items', cls_or_instance=fields.Nested(DocumentSchema))


class SearchDocumentSchema(DocumentSchema):
    summary = fields.String()


class SearchDocumentPaginationSchema(DocumentPaginationSchema):
    documents = fields.List(attribute='items', cls_or_instance=fields.Nested(SearchDocumentSchema))
