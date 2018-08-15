import os

from flask import current_app

from alexandria.modules.utils.exceptions import FileSizeError, FileTypeError

__author__ = 'oclay'


def validate_file_type(file, type):
    mimetype = file.mimetype
    extensions, max_size = [], 0
    if type is 'document':
        extensions = current_app.config['ALLOWED_DOCUMENT_EXT']
    elif type is 'image':
        extensions = current_app.config['ALLOWED_IMAGE_EXT']
    if mimetype and not mimetype.split('/')[1] in extensions:
        raise FileTypeError()


def get_file_size(file):
    chunk = 10
    while file.read(chunk) != b'':
        pass
    size = file.tell()
    file.seek(0, os.SEEK_SET)
    return size


def validate_file_size(file, max_size):
    size = get_file_size(file)
    if size > max_size:
        raise FileSizeError()


def similarity_detection():
    pass
