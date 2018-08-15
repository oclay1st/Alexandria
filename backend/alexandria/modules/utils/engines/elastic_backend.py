from math import ceil

from elasticsearch_dsl import DocType, field, Index, Q
from elasticsearch_dsl.connections import connections

from . import Engine

index = Index('alexandria_index')
index.settings(
    number_of_shards=1,
    number_of_replicas=0
)
ngram_analyzer = analyzer('my_analyzer',
    tokenizer=tokenizer('trigram', 'nGram', min_gram=2, max_gram=3),
    filter=['lowercase']
)

@index.doc_type
class Document(DocType):
    id = field.Integer()
    title = field.String(analyzer='snowball'),
    author = field.String(analyzer='snowball'),
    creation_date = field.Date(),
    pages = field.Integer(),
    content = field.String(analyzer='snowball'),
    lang = field.String(),
    size = field.Integer(),
    tags = field.String(index='not_analyzed')
    autocomplete = field.Text(analyzer = ngram_analyzer)


class ElasticEngine(Engine):
    def __init__(self, config):
        connections.create_connection(hosts=config['ELASTICSEARCH_HOST'], timeout=20)
        
        if index.exists() is False:
            index.create()

    def index_document(self, data):
        """
        Index a document
        :param data: set of data values per attributes to index
        :return: void
        """
        doc = Document(
            id=unicode(data['Id']),
            author=data['Author'],
            title=data['Title'],
            creation_date=data['CreationDate'],
            content=unicode(data['Content'], 'utf-8'),
            pages=data['NumPages'],
            size=data['Size'],
            lang=data['Lang'],
            tags=unicode(' '.join(data['Tags']), 'utf-8'),
            autocomplete = data['Title']
        )
        doc.save()

    def update_document(self, id, data):
        """
        Update the documents attributes
        :param id: document's identifier
        :param data: set of values per attributes
        :return: void
        """
        doc = Document.get(id=id)
        doc.update(**data)


    def delete_document(self, id):
        """
        Delete a document by id
        :param id: document's identifier
        :return: void
        """
        Document(id=id).delete()

    def delete_index(self):
        """Delete de current index"""
        index.delete()

    def search_ngram(self, args):
        """
        Get n-gram result ,when you typing it show the result
        :param args: The field to query like a title by example
        :return: a result list that matched
        """
        searcher = Document.search()
        searcher = searcher.query('match', autocomplete=args['criteria'])
        searcher = searcher.suggest('suggestions', args['criteria'], phrase={'field': 'autocomplete'})
        response = searcher[0:10].execute()
        for hit in response.hits.hits:
            print(hit.autocomplete)
        return {}


    def search_document(self, args):
        """
        Search all documents that match with the query
        :param args:  args from request to query
        :return: query result with pagination
        """
        searcher = Document.search()
        searcher = searcher.query(
            Q("match", title={'query': args['criteria'], 'boost': 3}) |
            Q("match", content=args['criteria'])
        ).highlight('content').source(exclude=["content"])
        searcher = self.create_filters(searcher, args)
        searcher = searcher.suggest('suggestions', args['criteria'], phrase={'field': 'title'})

        end = args['per_page'] * args['page']
        start = end - args['per_page']
        response = searcher[start:end].execute()
        return self.normalize_data(response, args)


    def create_filters(self, searcher, args):
        """
        :param searcher: Search instance
        :param args: args from request to filter
        :return: Search instance
        """
        filters = []
        if "author" in args:
            filters.append(Q("match", author=args['author']))
        if "tags" in args:
            filters.append(Q("terms", tags=args['tags']))
        if "lang" in args:
            filters.append(Q("match", lang=args['lang']))
        if len(filters):
            searcher = searcher.filter(Q('bool', must=filters))
        return searcher


    def normalize_data(self, response, args):
        """
        Normalize the response with pagination
        :param response: Response from elastic search
        :param args: The initial args from the request
        :return data: response normalized
        """
        data = {'items': [], 'id_list': []}
        for hit in response.hits.hits:
            result_dict = hit['_source']
            result_dict['summary'] = ','.join(hit['highlight']['content'])
            data['items'].append(result_dict)
            data['id_list'].append(int(result_dict['id']))
            data['suggestions'] = [sugg.text for sugg in response.suggest.suggestions]

        data['total'] = response.hits.total
        data['pages'] = int(ceil(response.hits.total / float(args['per_page'])))
        data['page'] = args['page']
        return data


    def rebuild_index(self):
        index.delete()
        index.create()
