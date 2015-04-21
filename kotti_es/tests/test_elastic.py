

class TestDefaultKottiAdapter:

    def test_kotti_adapter_iface(self):
        from pyramid_es.interfaces import IElastic
        from kotti_es.elastic import BaseElasticKottiContent
        adapter = BaseElasticKottiContent(None)
        assert IElastic.providedBy(adapter)

    def test_verify_adapter(self):
        from pyramid_es.interfaces import IElastic
        from kotti_es.elastic import BaseElasticKottiContent
        from zope.interface.verify import verifyObject
        adapter = BaseElasticKottiContent(None)
        assert verifyObject(IElastic, adapter)
