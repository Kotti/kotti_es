class TestIndexing:

    def test_insert(self, config, db_session, root, dummy_request):
        import transaction
        config.include('kotti_es')
        from kotti.resources import Document
        document = Document(title=u'mydoc', description=u'description',)
        document.request = dummy_request
        root[u'mydoc'] = document
        # with body=None no exceptions should be raised (utils/html_to_text)
        transaction.commit()
        from pyramid_es import get_client
        client = get_client(dummy_request)

        results = client.es.search(q='description')
        _type = results['hits']['hits'][0]['_type']
        assert _type == 'Document'
        assert results['hits']['hits'][0]['_source']['path'] == '/mydoc'

    def test_insert_searches(self, config, root, dummy_request):
        import transaction
        config.include('kotti_es')
        from kotti.resources import Document
        document = Document(title=u'title', description=u'description',
                            body=u'<span>body</span>')
        document.request = dummy_request
        root[u'mydoc'] = document
        # with body=None no exceptions should be raised (utils/html_to_text)
        transaction.commit()
        from pyramid_es import get_client
        client = get_client(dummy_request)

        assert len(client.es.search(q='title')['hits']['hits']) == 1
        assert len(client.es.search(q='description')['hits']['hits']) == 1
        # TODO: test failure, ok if you put a pdb
        # assert len(client.es.search(q='body')['hits']['hits']) == 1
        assert len(client.es.search(q='mydoc')['hits']['hits']) == 1
        assert len(client.es.search(q='span')['hits']['hits']) == 0
