# -*- coding: utf-8 -*-
"""Application configuration."""
import os
import logging
from dotenv import load_dotenv

__author__ = 'oclay'


class Config(object):
    """Base configuration."""

    # settings application path
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, os.pardir))
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

    # load evn vars
    load_dotenv(os.path.join(PROJECT_ROOT, '.env'))

    # setting secret key
    SECRET_KEY = os.getenv('SECRET_KEY', 'my-secret-key')

    # Files manage
    MAX_CONTENT_LENGTH = 200 * 1024 * 1024  # 200MB
    UPLOADS_DEFAULT_DEST = MEDIA_ROOT

    THUMBNAILS_ROOT = os.path.join(MEDIA_ROOT, 'thumbnails')
    PROFILES_ROOT = os.path.join(MEDIA_ROOT, 'profiles')
    DOCUMENTS_ROOT = os.path.join(MEDIA_ROOT, 'documents')
    MAX_DOCUMENT_SIZE = MAX_CONTENT_LENGTH
    MAX_IMAGE_SIZE = 1 * 1024 * 1024  # 1MB
    # max pdf pages
    MAX_PAGES = 200

    LOGGING_LOCATION = os.path.join(BASE_DIR, 'logs')

    ALLOWED_DOCUMENT_EXT = ['pdf']
    ALLOWED_IMAGE_EXT = ['jpg', 'png']
    UPLOADS_DEFAULT_URL = '/media'

    JWT_ACCESS_COOKIE_PATH = '/api/'
    JWT_COOKIE_SECURE = False  # TODO Change me on production

    BCRYPT_LOG_ROUNDS = 13
    # CACHE_TYPE = 'simple'  # TODO Can be "memcached", "redis", etc.

    # Flask Email configuration
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv('MAIL_PORT')
    MAIL_USE_TLS = bool(int(os.getenv('MAIL_USE_TLS', True)))
    MAIL_USERNAME = os.getenv('MAIL_PASSWORD')
    MAIL_PASSWORD = os.getenv('MAIL_USERNAME')

    # Registration config
    SEND_REGISTRATION_MAIL = True
    ACCOUNT_ACTIVATION_DAYS = 7

    # engines
    ENGINE = 'Whoosh'
    # ENGINE = 'ES'

    WHOOSH_INDEX = os.path.join(BASE_DIR, 'whoosh_index')

    ELASTICSEARCH_HOST = "localhost:9200"

    AUTH_BACKEND = 'Classic'
    # AUTH_BACKEND = 'LDAP'

    # available languages
    LANGUAGES = {
        'en': 'English',
        'es': 'Spanish'
    }

    # database configuration
    SQLALCHEMY_DATABASE_URI = '%s://%s:%s@%s:%s/%s' % (
        os.getenv('DB_DRIVER'),
        os.getenv('DB_USERNAME'),
        os.getenv('DB_PASSWORD'),
        os.getenv('DB_HOST'),
        os.getenv('DB_PORT'),
        os.getenv('DB_NAME')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MIGRATIONS_DIR = os.path.join(BASE_DIR, 'migrations')


class ProdConfig(Config):
    """Production configuration."""
    LOGGING_LEVEL = logging.WARNING


class DevConfig(Config):
    """
    Development configuration
    """
    DEBUG = True
    MAIL_DEBUG = True
    LOGGING_LEVEL = logging.DEBUG
    # SQLALCHEMY_ECHO = True
