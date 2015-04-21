from pytest import fixture


@fixture
def es_client(dummy_request, config):
    config.include('kotti_es')
    from pyramid_es import get_client
    client = get_client(dummy_request)
    client.es.indices.delete(index=client.index, ignore=[400, 404])
    client.flush()
    client.ensure_index(recreate=True)
    client.flush()
    return client


class TestIndexing:

    def test_insert(self, es_client, root, dummy_request):
        import transaction
        from kotti.resources import Document
        document = Document(title=u'mydoc', description=u'mydescription',)
        document.request = dummy_request
        root[u'mydoc'] = document
        # with body=None no exceptions should be raised (utils/html_to_text)
        transaction.commit()

        es_client.flush()
        results = es_client.es.search(q='mydescription')
        _type = results['hits']['hits'][0]['_type']
        assert _type == 'Document'
        assert results['hits']['hits'][0]['_source']['path'] == '/mydoc'

    def test_insert_searches(self, es_client, root,
                             dummy_request):
        import transaction
        from kotti.resources import Document
        document = Document(title=u'mytitle', description=u'mydescription',
                            body=u'<span>mybody</span>')
        document.request = dummy_request
        root[u'mydoc'] = document
        # with body=None no exceptions should be raised (utils/html_to_text)
        transaction.commit()

        es_client.flush()
        assert len(es_client.es.search(q='mytitle')['hits']['hits']) == 1
        assert len(es_client.es.search(q='mydescription')['hits']['hits']) == 1
        assert len(es_client.es.search(q='mybody')['hits']['hits']) == 1
        assert len(es_client.es.search(q='mydoc')['hits']['hits']) == 1
        assert len(es_client.es.search(q='span')['hits']['hits']) == 0

    def test_insert_delete(self, es_client, root,
                           dummy_request):
        import transaction
        from kotti.resources import Document
        document = Document(title=u'mytitle', description=u'mydescription',
                            body=u'<span>mybody</span>')
        document.request = dummy_request
        root[u'mydoc'] = document
        # with body=None no exceptions should be raised (utils/html_to_text)
        transaction.commit()

        es_client.flush()
        assert len(es_client.es.search(q='mytitle')['hits']['hits']) == 1

#        del root[u'mydoc']
#        transaction.commit()
#         es_client.flush()
#        assert len(es_client.es.search(q='title')['hits']['hits']) == 0
