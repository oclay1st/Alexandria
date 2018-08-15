__author__ = 'oclay'


class Engine(object):
    """
    Interface  for supported engines :whoosh and elasticsearch at the moment
    """

    def __inti__(self, config):
        pass

    def index_document(self, data):
        raise NotImplementedError

    def update_document(self, id, data):
        raise NotImplementedError

    def delete_document(self, id):
        raise NotImplementedError

    def delete_index(self):
        raise NotImplementedError

    def search_ngram(self, params):
        raise NotImplementedError

    def search_document(self, params):
        raise NotImplementedError

    def rebuild_index(self):
        raise NotImplementedError
