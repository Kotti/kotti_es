class TestEvents:

    def test_wire_sqlalchemy(self):
        from kotti_es.events import _WIRED_SQLALCHEMY
        assert _WIRED_SQLALCHEMY is True

        from kotti_es.events import wire_sqlalchemy
        import mock
        with mock.patch('kotti_es.events.sqlalchemy.event.listen') as listen:
            wire_sqlalchemy()
            assert listen.call_args_list == []
