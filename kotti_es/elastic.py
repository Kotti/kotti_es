from zope.interface import (
    implements,
    )
from zope.component import (
    adapts,
    )
from kotti.interfaces import (
    IDocument,
    IContent,
    )
from pyramid_es.mixin import ESMapping, ESString
from .interfaces import IElastic


class ElasticBase(object):

    def __init__(self, context):
        self.context = context

    @classmethod
    def elastic_mapping(cls):
        """
        Return an ES mapping.
        """
        raise NotImplementedError("ES classes must define a mapping")

    def elastic_document(self):
        """
        Apply the class ES mapping to the current context
        """
        return self.elastic_mapping()(self.context)


class ElasticContent(ElasticBase):
    implements(IElastic)
    adapts(IContent)

    @classmethod
    def elastic_mapping(cls):
        """
        Return an ES mapping.
        """
        return ESMapping(
            attr='context',
            analyzer='content',
            properties=ESMapping(
                ESString('description', boost=5.0)))


class ElasticDocument(ElasticBase):
    implements(IElastic)
    adapts(IDocument)

    @classmethod
    def elastic_mapping(cls):
        """
        Return an ES mapping.
        """
        return ESMapping(
            attr='context',
            analyzer='content',
            properties=ESMapping(
                ESString('description', boost=5.0)))
