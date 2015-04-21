class TestIndexing:

    def test_insert(self, config, db_session, root, dummy_request):
        import transaction
        config.include('kotti_es')
        from kotti.resources import Document
        document = Document(title='mydoc', description='description',)
        document.request = dummy_request
        root['mydoc'] = document
        transaction.commit()
        from pyramid_es import get_client
        client = get_client(dummy_request)

        results = client.es.search(q='description')
        _type = results['hits']['hits'][0]['_type']
        assert _type == 'Document'
        assert results['hits']['hits'][0]['_source']['path'] == '/mydoc'
