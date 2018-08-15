from flask_babel import gettext as _

__author__ = 'oclay'


class FileTypeError(Exception):
    """
    Exception for files type
    """

    def __init__(self):
        self.message = _("Document type not allowed")

    def __str__(self):
        return self.message


class FileSizeError(Exception):
    """
    Exception for file size
    """

    def __init__(self):
        self.message = _("Document size not allowed")

    def __str__(self):
        return self.message
