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
