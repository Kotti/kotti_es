class TestEvents:

    def test_wire_sqlalchemy(self):
        from kotti_es.events import _WIRED_SQLALCHEMY
        assert _WIRED_SQLALCHEMY is True

        from kotti_es.events import wire_sqlalchemy
        import mock
        with mock.patch('kotti_es.events.sqlalchemy.event.listen') as listen:
            wire_sqlalchemy()
            assert listen.call_args_list == []

    def test_after_insert(self, dummy_request):
        from kotti.resources import Document
        document = Document()
        document.id = 1
        document.request = dummy_request
        assert hasattr(document.request, '_index_list') is False
        from kotti_es.events import _after_insert_update
        from kotti_es.events import INSERT_CODE
        _after_insert_update(None, None, document)
        assert getattr(document.request, '_index_list') == [
            (document.id, INSERT_CODE)
            ]

    def test_after_delete(self, dummy_request):
        from kotti.resources import Document
        document = Document()
        document.id = 1
        document.request = dummy_request
        assert hasattr(document.request, '_index_list') is False
        from kotti_es.events import _after_delete
        from kotti_es.events import DELETE_CODE
        _after_delete(None, None, document)
        assert getattr(document.request, '_index_list') == [
            (document.id, DELETE_CODE)
            ]

    def test_after_delete2(self, dummy_request):
        from kotti.resources import Document
        document = Document()
        document.id = 1
        document.request = dummy_request
        document.request._index_list = []
        from kotti_es.events import _after_delete
        from kotti_es.events import DELETE_CODE
        _after_delete(None, None, document)
        assert getattr(document.request, '_index_list') == [
            (document.id, DELETE_CODE)
            ]

    def test_after_delete3(self, dummy_request):
        from kotti.resources import Document
        document1 = Document()
        document1.request = dummy_request
        document2 = Document()
        document2.request = dummy_request
        from kotti_es.events import _after_delete
        _after_delete(None, None, document1)
        _after_delete(None, None, document2)
        assert len(getattr(dummy_request, '_index_list')) == 2

    def test_after_commit_insert(self, dummy_request):
        from kotti.resources import Document
        from kotti_es.events import _after_insert_update
        from kotti_es.events import _after_commit
        document = Document()
        document.request = dummy_request
        _after_insert_update(None, None, document)

        import mock
        with mock.patch('kotti_es.events.get_current_request') as \
                get_current_request:
            get_current_request.return_value = dummy_request
            with mock.patch('kotti_es.events.get_client') as \
                    get_client:
                magic = mock.MagicMock()
                get_client.return_value = magic
                session = mock.Mock()
                session.configure_mock(**{
                    'query.return_value.filter_by.'
                    'return_value.one.return_value': document})
                _after_commit(session)
                magic.index_object.assert_called_with(document,
                                                      immediate=True)

    def test_after_commit_delete(self, dummy_request):
        from kotti.resources import Document
        from kotti_es.events import _after_delete
        from kotti_es.events import _after_commit
        document = Document()
        document.request = dummy_request
        _after_delete(None, None, document)

        import mock
        with mock.patch('kotti_es.events.get_current_request') as \
                get_current_request:
            get_current_request.return_value = dummy_request
            with mock.patch('kotti_es.events.get_client') as \
                    get_client:
                magic = mock.MagicMock()
                get_client.return_value = magic
                session = mock.Mock()
                session.configure_mock(**{
                    'query.return_value.filter_by.'
                    'return_value.one.return_value': document})
                _after_commit(session)
                magic.delete_object.assert_called_with(document,
                                                       immediate=True)
