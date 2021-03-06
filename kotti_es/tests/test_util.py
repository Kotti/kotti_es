from unittest import TestCase


class TestUtil(TestCase):

    def test_blacklistfromsettings(self):
        settings = {'kotti_es.blacklist': u'\nDocument\nFile'}
        from kotti_es.util import blacklist_from_settings
        blacklist = blacklist_from_settings(settings)
        self.assertEquals(['Document', 'File'], blacklist)

    def test_blacklistfromsettings_empty(self):
        settings = {'kotti_es.blacklist': u''}
        from kotti_es.util import blacklist_from_settings
        blacklist = blacklist_from_settings(settings)
        self.assertEquals([], blacklist)

    def test_blacklistfromsettings_empty2(self):
        settings = {}
        from kotti_es.util import blacklist_from_settings
        blacklist = blacklist_from_settings(settings)
        self.assertEquals([], blacklist)

    def test_get_request(self):
        class Target:
            def __init__(self, request):
                self.request = request
        from pyramid.testing import DummyRequest
        from kotti_es.util import get_request
        request = DummyRequest()
        target = Target(request)
        self.assertEquals(request, get_request(target))

    def test_get_request_current(self):
        class Target:
            pass
        from pyramid.testing import DummyRequest
        from kotti_es.util import get_request
        request = DummyRequest()
        target = Target()
        import mock
        with mock.patch('kotti_es.util.get_current_request') as mock_request:
            mock_request.return_value = request
            result_request = get_request(target)
        self.assertEquals(request, result_request)

    def test_is_blacklisted_no_icontent(self):
        from kotti_es.util import is_blacklisted

        class Target:
            pass
        target = Target()
        self.assertTrue(is_blacklisted(target))

    def test_is_blacklisted_icontent_no_request(self):
        from kotti_es.util import is_blacklisted
        from kotti.interfaces import IContent
        from kotti.resources import TypeInfo
        from zope.interface import implements

        class Target:
            implements(IContent)
            type_info = TypeInfo(name='pippo')
        target = Target()

        import mock
        with mock.patch('kotti_es.util.get_current_registry') as mock_registry:
            settings = {'kotti_es.blacklist': []}
            mock_registry.return_value = mock.Mock(settings=settings)
            self.assertFalse(is_blacklisted(target))

    def test_is_blacklisted_icontent_no_request_blacklisted(self):
        from kotti_es.util import is_blacklisted
        from kotti.interfaces import IContent
        from kotti.resources import TypeInfo
        from zope.interface import implements

        class Target:
            implements(IContent)
            type_info = TypeInfo(name='pippo')
        target = Target()

        import mock
        with mock.patch('kotti_es.util.get_current_registry') as mock_registry:
            settings = {'kotti_es.blacklist': ['pippo']}
            mock_registry.return_value = mock.Mock(settings=settings)
            self.assertTrue(is_blacklisted(target))

    def test_is_blacklisted_icontent_request(self):
        from kotti_es.util import is_blacklisted
        from kotti.interfaces import IContent
        from kotti.resources import TypeInfo
        from zope.interface import implements

        class Target:
            implements(IContent)
            type_info = TypeInfo(name='pippo')

            def __init__(self, request):
                self.request = request
        import mock
        settings = {'kotti_es.blacklist': []}
        request = mock.Mock(registry=mock.Mock(settings=settings))
        target = Target(request)

        self.assertFalse(is_blacklisted(target))

    def test_html_to_text(self):
        from kotti_es.util import html_to_text
        value = ''.join([
            "<span>Foo</span> Bar <script type='text/javascript'>",
            "var xyz = 1;</script>",
            ])
        filtered = html_to_text(value)
        self.assertTrue('Foo' in filtered)
        self.assertTrue('Bar' in filtered)
        self.assertFalse('span' in filtered)
        self.assertFalse('script' in filtered)
        self.assertFalse('xyz' in filtered)

    def test_search(self):
        from kotti_es.util import es_search_content
        import mock

        with mock.patch('kotti_es.util.get_client') as get_client:
            es = mock.Mock()
            es.search = lambda *args, **kwargs: {'hits': {'hits': []}}
            client = mock.Mock()
            client.es = es
            get_client.return_value = client

            assert es_search_content('pippo') == []
