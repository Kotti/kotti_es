

class TestDefaultKottiAdapter:

    def test_kotti_adapter_iface(self):
        from pyramid_es.interfaces import IElastic
        from kotti_es.elastic import BaseElasticKottiContent
        from kotti.resources import Document
        adapter = BaseElasticKottiContent(Document())
        assert IElastic.providedBy(adapter)

    def test_verify_adapter(self):
        from pyramid_es.interfaces import IElastic
        from kotti_es.elastic import BaseElasticKottiContent
        from zope.interface.verify import verifyObject
        from kotti.resources import Document
        adapter = BaseElasticKottiContent(Document())
        assert verifyObject(IElastic, adapter)

    def test_verify_document(self, root):
        from kotti.resources import Document
        from kotti_es.elastic import BaseElasticKottiContent
        document = Document(title=u'mytitle',
                            description=u'mydescr',
                            body=u'<span>hello</span>')
        root[u'document'] = document
        assert root[u'document'].name == u'document'

        adapter = BaseElasticKottiContent(document)
        assert adapter.elastic_document_type() == document.type_info.name
        assert adapter.elastic_document_id() == document.id

    def test_verify_document_default_mapping(self, root):
        from kotti.resources import Document
        from kotti_es.elastic import BaseElasticKottiContent
        document = Document(title=u'mytitle',
                            description=u'mydescr',
                            body=u'<span>hello</span>')
        root[u'document'] = document
        assert root[u'document'].name == u'document'

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
        document = Document(title=u'mytitle',
                            description=u'mydescr',
                            body=u'<span>hello</span>')
        root[u'document'] = document
        assert root[u'document'].name == u'document'

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

    def test_verify_document_default_mapping_attrs_methods(self, root):
        from kotti.resources import Document
        from kotti_es.elastic import BaseElasticKottiContent
        document = Document(title=u'mytitle',
                            description=u'mydescr',
                            body=u'<span>hello</span>')
        root[u'document'] = document
        assert root[u'document'].name == u'document'

        adapter = BaseElasticKottiContent(document)

        assert adapter._title == document.title
        assert adapter._description == document.description
        assert adapter._body == document.body
        assert adapter._path == document.path
        assert adapter._name == document.name
        assert adapter._id == document.id

    def test_verify_document_type_info_mapping(self, root):
        from kotti.resources import Document
        from kotti_es.elastic import BaseElasticKottiContent
        document = Document(title=u'mytitle',
                            description=u'mydescr',
                            body=u'<span>hello</span>')
        document.type_info.elastic_mapping = 1
        root[u'document'] = document
        assert root[u'document'].name == u'document'

        adapter = BaseElasticKottiContent(document)
        assert adapter.elastic_mapping() == 1
        del document.type_info.elastic_mapping

    def test_component_lookup(self, config, root):
        from kotti.resources import Document
        from pyramid_es.interfaces import IElastic
        from kotti_es.elastic import BaseElasticKottiContent
        document = Document(title=u'mytitle',
                            description=u'mydescr',
                            body=u'<span>hello</span>')
        config.include('kotti_es')
        adapter = config.registry.queryAdapter(document, IElastic)
        assert adapter is not None
        assert isinstance(adapter, BaseElasticKottiContent)
