# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
import os
from logging.handlers import RotatingFileHandler
from jwt import exceptions as jwt_exceptions
from flask import Flask, jsonify, render_template, send_from_directory
from flask_jwt_extended import exceptions as flask_jwt_exceptions
from flask_uploads import configure_uploads, patch_request_class
from alexandria.settings import commands
from alexandria.modules.core.views import blueprint as core_blueprint
from alexandria.modules.security.views import blueprint as security_blueprint
from alexandria.settings.config import ProdConfig
from alexandria.settings.extensions import *

__author__ = 'oclay'


def create_app(config_object=ProdConfig()):
    """
    An application factory
    :param config_object: The configuration object to use.
    """
    app = Flask('alexandria', static_folder='static')
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_media_url(app)
    register_upload_files(app)
    register_error_handlers(app)
    register_shellcontext(app)
    register_commands(app)
    register_logger(app)
    register_engine(app)    
    return app


def register_extensions(app):
    """
    Register Flask extensions.
    :param app Application instance
    """    
    corsd.init_app(app)
    rq.init_app(app)
    jwt.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    api.init_app(app)
    es.init_app(app)
    babel.init_app(app)
    migrate.init_app(app, db, directory=app.config['MIGRATIONS_DIR'])
    # socketio.init_app(app)


def register_blueprints(app):
    """
    Register Flask blueprints.
    :param app Application instance
    """
    app.register_blueprint(core_blueprint)
    app.register_blueprint(security_blueprint)


def __api_authorized_error(error):
    """Return error api authorization."""
    return {'message': str(error)}, getattr(error, 'code', 401)


def __render_error(error):
    """Render error template."""
    # If a HTTPException, pull the `code` attribute; default to 500
    error_code = getattr(error, 'code', 500)
    return render_template('{0}.html'.format(error_code)), error_code


def __webargs_error_handler(err):
    exc = err.exc
    return jsonify({'messages': exc.messages}), 422


def register_error_handlers(app):
    """Register error handlers.
    :param app Application instance"""
    exceptions = flask_jwt_exceptions.__dict__.items() + jwt_exceptions.__dict__.items()
    for name, cls in exceptions:
        if isinstance(cls, type):
            api.errorhandler(cls)(__api_authorized_error)

    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(__render_error)

    app.errorhandler(422)(__webargs_error_handler)


def register_shellcontext(app):
    """Register shell context objects.
    :param app Application instance"""

    def shell_context():
        """Shell context objects."""
        return {}

    app.shell_context_processor(shell_context)


def register_commands(app):
    """Register Click commands.
    :param app Application instance"""
    app.cli.add_command(commands.clean)
    app.cli.add_command(commands.remove_files)
    app.cli.add_command(commands.rebuild_index)
    app.cli.add_command(commands.create_admin)
    app.cli.add_command(commands.remove_activation_expired)


def register_media_url(app):
    """Register media files urls
    :param app Application instance"""

    def get_media_dir(path):
        return send_from_directory(app.config['MEDIA_ROOT'], path)

    app.add_url_rule('/media/<path:path>', 'media',
                     lambda path, application=app: get_media_dir(path))


def register_upload_files(app):
    """
    Register uploaded files
    :param app Application instance
    """
    configure_uploads(app, (document_file, profile_image, thumbnail_image))
    patch_request_class(app, 200 * 1024 * 1024)


def register_logger(app):
    """
    Register logger into a file
    :param app Application instance
    """
    if app.config['ENV'] == 'prod':
        log_file = os.path.join(app.config['LOGGING_LOCATION'], 'error.log')
        handler = RotatingFileHandler(log_file,
                                      maxBytes=90000, backupCount=1)
        handler.setLevel(app.config['LOGGING_LEVEL'])
        app.logger.addHandler(handler)


def register_engine(app):
    """
    Register engine
    :param app: Application instance
    """
    if hasattr(app, 'engine'):
        raise Exception('Engine already initialized')
    with app.app_context():
        def get_engine():
            if app.config['ENGINE'] == 'Whoosh':
                from alexandria.modules.utils.engines.whoosh_backend import WhooshEngine
                return WhooshEngine(app.config)
            elif app.config['ENGINE'] == 'ES':
                from alexandria.modules.utils.engines.elastic_backend import ElasticEngine
                return ElasticEngine(app.config)
            else:
                raise Exception(
                    'Engine settings error: [\'{}\'] no supported'.format(app.config['ENGINE']))

        setattr(app, 'engine', get_engine())
