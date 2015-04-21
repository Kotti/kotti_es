

class TestSettings:

    def test_kotti_es_configure(self):
        from kotti_es import kotti_configure
        settings = {'pyramid.includes': ''}
        kotti_configure(settings)
        assert 'kotti_es' in settings['pyramid.includes']

    def test_kotti_es_configure2(self):
        from kotti_es import kotti_configure
        settings = {'pyramid.includes': 'pippo'}
        kotti_configure(settings)
        assert 'kotti_es' in settings['pyramid.includes']
        assert 'pippo' in settings['pyramid.includes']
        assert settings['pyramid.includes'] == 'pippo kotti_es'
