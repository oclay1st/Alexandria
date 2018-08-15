# -*- coding: utf-8 -*-
import os
import shutil

from whoosh import highlight
from whoosh.analysis import StandardAnalyzer, NgramFilter
from whoosh.fields import Schema, TEXT, ID, KEYWORD, DATETIME, STORED
from whoosh.index import create_in, open_dir
from whoosh.qparser import MultifieldParser, QueryParser, OrGroup
from whoosh.qparser.dateparse import DateParserPlugin

from . import Engine

try:
    UNICODE_EXISTS = bool(type(unicode))
except NameError:
    unicode = lambda s: str(s)

__author__ = 'oclay'


class WhooshEngine(Engine):
    def __init__(self, config):
        self.schema = Schema(
            id=ID(unique=True),
            title=TEXT(stored=True, field_boost=3.0, analyzer=StandardAnalyzer() | NgramFilter(minsize=2, maxsize=3)),
            author=TEXT(stored=True),
            creation_date=DATETIME(stored=True),
            pages=STORED,
            content=TEXT(stored=True, analyzer=StandardAnalyzer(stoplist=None)),
            lang=TEXT(stored=True),
            size=STORED,
            tags=KEYWORD(stored=True, commas=True)
        )

        self.index_path = config['WHOOSH_INDEX']

        if not os.path.exists(self.index_path):
            os.mkdir(self.index_path)
            create_in(self.index_path, self.schema)

        self.indexer = open_dir(self.index_path)
        self.parser_content = MultifieldParser(["title", "content"], schema=self.schema)
        self.parser_content.add_plugin(DateParserPlugin())
        self.date_format = {
            'last_24h': u'-24h to now',
            'last_week': u'last week',
            'last_month_to_now': u'-1mo to now',
            'last_year_to_now': u"[-2yrs to now]"
        }

    def index_document(self, data):
        """
        Index a document
        :param data: set of data values per attributes to index
        :return: void
        """
        writer = self.indexer.writer()
        writer.add_document(
            id=unicode(data['Id']),
            author=data['Author'],
            title=data['Title'],
            creation_date=data['CreationDate'],
            content=unicode(data['Content'], 'utf-8'),
            pages=data['NumPages'],
            size=data['Size'],
            lang=data['Lang'],
            tags=unicode(','.join(data['Tags']), 'utf-8')
        )
        writer.commit()

    def update_document(self, id, data):
        """
        Update the documents attributes
        :param id: document's identifier
        :param data: set of values per attributes
        :return: void
        """
        writer = self.indexer.writer()
        data['id'] = unicode(id)
        writer.update_document(**data)
        writer.commit()

    def delete_document(self, id):
        """
        Delete a document by id
        :param id: document's identifier
        :return: void
        """
        self.indexer.delete_by_term('id', unicode(id))
        self.indexer.commit()

    def delete_index(self):
        """Delete de current index"""
        create_in(self.index_path, schema=self.schema)

    def search_ngram(self, args):
        """
        Get n-gram result ,when you typing it show the result
        :param args: The field to query like a title by example
        :return data: a result list that matched
        """
        criteria = args['criteria']
        with self.indexer.searcher() as searcher:
            simple_parser = QueryParser("title", group=OrGroup, schema=self.schema)
            query = simple_parser.parse(criteria)
            response = searcher.search_page(query, pagenum=1)
            data = [result['title'] for result in response.results]
            return data

    def search_document(self, args):
        """
        Search all documents that mach with the query
        :param args:  params from request to query
        :return: query result with pagination
        """
        with self.indexer.searcher() as searcher:
            query = self.parser_content.parse(args['criteria'])
            filters = self.create_filters(args)

            response = searcher.search_page(query, pagenum=args['page'], filter=filters)

            return self.normalize_data(response)

    def create_filters(self, args):
        """
        :param args: params from request to filter
        :return: Search instance
        """
        allow_list = []
        if "creation_date" in args:
            # :creation date format ex: creation_date:[last week to now]
            date_query = 'creation_date:' + self.date_format[args["creation_date"]]
            allow_list.append(date_query)

        if "lang" in args:
            # :lang format ex: (lang:es OR lang:en)
            lang_list = ['lang:' + lang for lang in args['lang']]
            lang_query = ' OR '.join(lang_list)
            allow_list.append('(' + lang_query + ')')

        if "author" in args:
            # :autor format ex: (author:Antonio)
            author_query = 'author:' + args['author']
            allow_list.append('(' + author_query + ')')

        if "tags" in args:
            # :tags format ex: (tag:'history' OR tag:'docker')
            tag_list = ['tags:' + tag for tag in args['tags']]
            tag_query = ' OR '.join(tag_list)
            allow_list.append('(' + tag_query + ')')
        # : all filters
        query_string = u' AND '.join(allow_list)
        return self.parser_content.parse(query_string) if query_string else None

    def normalize_data(self, response):
        """
        Normalize the response adding pagination
        :param response: Response from elastic search  
        :return: data normalized
        """
        data = {'items': [], 'id_list': []}
        response.results.fragmenter.surround = 80  #: summary length
        # page_result.results.fragmenter.maxchars = 300
        my_cf = highlight.SentenceFragmenter()
        # page_result.results.fragmenter = my_cf
        for result in response.results:
            # print result.title
            result_dict = dict(result)
            result_dict['summary'] = result.highlights("content", top=2)
            data['items'].append(result_dict)
            data['id_list'].append(int(result_dict['id']))

        data['total'] = response.total
        data['pages'] = response.pagecount
        data['page'] = response.pagenum
        return data

    def rebuild_index(self):
        shutil.rmtree(self.index_path)
        os.mkdir(self.index_path)
        create_in(self.index_path, schema=self.schema)
