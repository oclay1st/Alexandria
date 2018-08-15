from flask import render_template, Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_claims

from alexandria.modules.utils.util import get_current_user_jwt
from alexandria.modules.utils.vendor.flask_restplus_patched import Resource, Namespace
from alexandria.settings.extensions import api, babel
from serializers import *
from utils import *

__author__ = 'oclay'

blueprint = Blueprint('alexandria', __name__)

core_api = Namespace('Core', path='/')
api.add_namespace(core_api)


@blueprint.route('/')
def home():
    return render_template('home.html')


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'].keys())


@core_api.route('/search')
class SearchView(Resource):
    """
    Api endpoint for search documents
    """

    @core_api.response(SearchDocumentPaginationSchema())
    @core_api.parameters(SearchSchema(), locations=('query',))
    def get(self, args):
        return search_documents(args)


@core_api.route('/suggestions')
class SearchNGramView(Resource):
    """
    Api endpoint for search documents
    """

    @core_api.parameters(SearchBaseSchema())
    def get(self, args):
        return jsonify({'suggestions': search_ngram(args)})


@core_api.route('/documents')
class DocumentsView(Resource):
    """
    Api endpoint for list documents or create one
    """

    @core_api.response(DocumentPaginationSchema())
    @core_api.parameters(PageSchema(), locations=('query',))
    def get(self, args):
        return list_documents(args)

    @jwt_required
    @core_api.parameters(UploadSchema(), locations=('form', 'json',))
    def post(self, args):
        user = get_current_user_jwt()
        response = create_document(args, user)
        if not response['create']:
            return response, 401
        return response


@core_api.route('/document/<int:id>')
class DocumentDetailView(Resource):
    """
    Api endpoint for a document crud:create,update
    """

    @core_api.response(DocumentSchema())
    def get(self, id):
        return get_document(id)

    @jwt_required
    @core_api.parameters(UpdateSchema(), as_kwargs=True, locations=('form', 'json',))
    def patch(self, id, **kwargs):
        response = update_document(id, kwargs)
        if not response['update']:
            return response, 403
        return response


@core_api.route('/document/<int:id>/favorite')
class DocumentFavoriteView(Resource):
    """
    Api endpoint for a favorite document
    """

    @jwt_required
    def post(self, id):
        user = get_current_user_jwt()
        return add_to_favorites(id, user)

    @jwt_required
    def delete(self, id):
        user = get_current_user_jwt()
        return remove_from_favorites(id, user)


@core_api.route('/documents/favorites')
class DocumentFavoritesView(Resource):
    """
    Api endpoint for a favorite document
    """

    @jwt_required
    @core_api.response(DocumentPaginationSchema())
    @core_api.parameters(PageSchema(), locations=('query',))
    def get(self, args):
        claims = get_jwt_claims()
        return list_favorites(claims['id'], args)


@core_api.route('/documents/tag/<string:tag>')
class TagsView(Resource):
    """
    Api endpoint for document's tag
    """

    @core_api.response(DocumentPaginationSchema())
    def get(self, tag):
        return get_documents_by_tag(tag)
