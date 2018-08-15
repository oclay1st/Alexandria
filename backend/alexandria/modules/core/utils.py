import six
from flask import current_app as app
from flask_babel import gettext as _
from flask_uploads import UploadNotAllowed
from werkzeug.exceptions import abort

from alexandria.modules.security.models import user_favorite_documents
from alexandria.modules.utils.exceptions import FileTypeError
from alexandria.modules.utils.parsers.parser import PDFParser
from alexandria.modules.utils.util import admin_permission
from alexandria.modules.utils.validators.files import validate_file_type, get_file_size
from alexandria.settings.extensions import document_file
from alexandria.settings.extensions import thumbnail_image, db
from models import Document
from permissions import is_document_owner
from signals import document_created_signal
from serializers import DocumentSchema


def search_ngram(args):
    result = app.engine.search_ngram(args)
    return result


def search_documents(args):
    results = app.engine.search_document(args)  #: contains title,resume,creation_date,upload_date,language
    if not results['items']:
        abort(404)
    documents = Document.query.options(joinedload('user')).filter(Document.id.in_(results['id_list']))
    for i, document in enumerate(documents):
        results['items'][i]['file_url'] = document.file_url
        results['items'][i]['thumbnail_url'] = document.thumbnail_url
        results['items'][i]['upload_date'] = document.upload_date
        results['items'][i]['likes'] = document.likes
        results['items'][i]['user'] = document.user.username
    return results


def get_document(document_id):
    return Document.query.get_or_404(document_id)


def list_documents(args):
    """
    List documents
    :param args: pagination data
    :return a list of documents
    """
    page = args['page']
    per_page = args['page'] if 'per_page' in args else 10
    documents = Document.query.order_by(
        Document.upload_date.desc()).paginate(page=page, per_page=per_page)
    return documents


def update_document(document_id, args):
    """
    Update the document data
    :param document_id: document identifaier
    :param args: data to set
    :return: a dict, update True if the document was successfull updated or False if not
    """
    document = Document.query.get_or_404(document_id)
    # removing args with missing values
    data = {key: value for key, value in six.iteritems(args) if value}
    if is_document_owner(document) or admin_permission.can():
        for arg in data:
            setattr(document, arg, data[arg])
        db.session.commit()
        app.engine.update_document(document_id, data)
        return {'message': _('document modified success'), 'updated': True}
    return {'message': _('permission denied'), 'updated': False}


def create_document(args, user):
    """
    Create a new document, store and indexing the data
    :param args: document data
    :param user: current user
    :return: create True if the document is created successfull or False if not
    """
    try:
        validate_file_type(args['document'], 'document')
        file_size = get_file_size(args['document'])
        filename = document_file.save(args['document'])
        document = Document(filename=filename, size=file_size)
        # : define document's parser
        parser = PDFParser(document.file, max_pages=app.config['MAX_PAGES'])
        # : extracting metadata
        metadata = parser.read_metadata()
        # : generating thumbnail
        thumb_name = generate_thumbnail(parser)
        document.thumbnail = thumb_name
        # : saving the document
        save_document(document, metadata, user)
        # :indexing document
        index_document(document, metadata)
        return {'create': True, 'message': _('Success creation')}
    except UploadNotAllowed:
        return {'create': False, 'message': _('Name of document has errors')}
    except FileTypeError as ex:
        return {'create': False, 'message': ex.message}


def generate_thumbnail(parser):
    """
    Generate a thumbnail from the document file
    :param parser: file's parser
    :return: thumbnail name
    """
    scale_x, scale_y, thumb_name = 120, 160, parser.name + '.png'
    thumb_path = thumbnail_image.path(thumb_name)
    parser.generate_thumbnail(thumb_path, scale_x, scale_y)
    return thumb_name


def save_document(document, metadata, user):
    """
    Save the document into the database
    :param document: document object
    :param data: data to set
    :param user: the owner
    :return: void
    """
    document.author = metadata['Author']
    document.lang = metadata['Lang']
    document.pages = metadata['NumPages']
    document.creation_date = metadata['CreationDate']
    document.title = metadata['Title']
    user.documents.append(document)
    db.session.commit()


def index_document(document, metadata):
    """
    Index document into the engine
    :param data: data to set
    :param document: document object
    :return: void
    """
    metadata['Tags'] = ['sss']
    metadata['Id'] = document.id
    metadata['Size'] = document.size
    document_created_signal.send(app._get_current_object(), data=metadata)


def list_favorites(user_id, args):
    """
    List favorites documents of an user
    :param user_id: user identifaier
    :param args: pagination data
    :return: a list of documents
    """
    page = args['page']
    per_page = args['page'] if 'per_page' in args else 10
    documents = Document.query.filter(
        Document.users.any(id=user_id)).paginate(page=page, per_page=per_page)
    return documents


def is_favorite(user, document_id):
    """
    Check if the document is favorite
    :param user: user object
    :param document_id: document identifaier
    :return: boolean
    """
    return user.favorite_documents.filter(user_favorite_documents.c.document_id == document_id).count() > 0


def add_to_favorites(document_id, user):
    """
    Add document to favorites
    :param document_id: document id
    :param user: user object
    :return dict: a message
    """
    if not is_favorite(user, document_id):
        document = Document.query.filter_by(id=document_id).first()
        user.favorite_documents.append(document)
        db.session.commit()
        return {'message': _('The document was added to favorites'), 'add_to_favorites': True}
    return {'message': _('The document is already part of yours favorites'), 'add_to_favorites': False}


def remove_from_favorites(document_id, user):
    """
    Revome document from favorites
    :param document_id: document's id
    :param user: user object
    :return dict: a message
    """
    if is_favorite(user, document_id):
        document = Document.query.filter_by(id=document_id).first()
        user.favorite_documents.remove(document)
        db.session.commit()
        return {'message': _('Document removed from favorites')}
    return {'message': _('The document is not present in yours favorite documents')}


def get_documents_by_tag(tags):
    return Document.query.filter(Document.tags.id.in_([tags]))
