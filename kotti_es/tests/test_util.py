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
