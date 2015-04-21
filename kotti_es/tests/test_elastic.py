

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

    def test_verify_document(self, root):
        from kotti.resources import Document
        from kotti_es.elastic import BaseElasticKottiContent
        document = Document(title='mytitle',
                            description='mydescr',
                            body='<span>hello</span>')
        root['document'] = document
        assert root['document'].name == 'document'

        adapter = BaseElasticKottiContent(document)
        assert adapter.elastic_document_type() == document.type_info.name
        assert adapter.elastic_document_id() == document.id
