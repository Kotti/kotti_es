

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

    def test_verify_document_default_mapping(self, root):
        from kotti.resources import Document
        from kotti_es.elastic import BaseElasticKottiContent
        document = Document(title='mytitle',
                            description='mydescr',
                            body='<span>hello</span>')
        root['document'] = document
        assert root['document'].name == 'document'

        adapter = BaseElasticKottiContent(document)
        elastic_mapping = adapter.elastic_mapping()
        es_mapping_props = elastic_mapping.properties
        assert 'title' in es_mapping_props
        assert 'description' in es_mapping_props
        assert 'body' in es_mapping_props
        assert 'path' in es_mapping_props
        assert '_id' in es_mapping_props
        assert 'name' in es_mapping_props

    def test_verify_document_default_mapping_attrs(self, root):
        from kotti.resources import Document
        from kotti_es.elastic import BaseElasticKottiContent
        document = Document(title='mytitle',
                            description='mydescr',
                            body='<span>hello</span>')
        root['document'] = document
        assert root['document'].name == 'document'

        adapter = BaseElasticKottiContent(document)
        elastic_mapping = adapter.elastic_mapping()
        es_mapping_props = elastic_mapping.properties
        assert es_mapping_props['title'].attr == '_title'
        assert es_mapping_props['description'].attr == '_description'
        assert es_mapping_props['body'].attr == '_body'
        from kotti_es.util import html_to_text
        assert es_mapping_props['body'].filter == html_to_text
        assert es_mapping_props['path'].attr == '_path'
        assert es_mapping_props['_id'].attr is None
        assert es_mapping_props['name'].attr == '_name'
