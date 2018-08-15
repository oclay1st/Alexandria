from blinker import Namespace

__author__ = 'oclay'

signals = Namespace()

document_created_signal = signals.signal('document_created')

document_updated_signal = signals.signal('document_updated')


@document_created_signal.connect
def index_new_document(sender, data):
    sender.engine.index_document(data)


@document_updated_signal.connect
def refresh_document_indexed(sender, data):
    sender.engine.update_document(data)

