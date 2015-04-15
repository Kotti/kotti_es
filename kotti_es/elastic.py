from zope.component import (
    adapts,
    )
from kotti.interfaces import (
    IContent,
    )
from pyramid_es.mixin import (
    ESMapping,
    ESString,
    )
from pyramid_es.elastic import ElasticBase


class ElasticContent(ElasticBase):
    adapts(IContent)

    @classmethod
    def elastic_mapping(cls):
        """
        Return an ES mapping.
        """
        # TODO: return all mappings dynamically
        return ESMapping(
            attr='context',
            analyzer='content',
            properties=ESMapping(
                ESString('description', boost=5.0)))

    def elastic_document_type(self):
        """
        The elastic document type
        """
        return self.context.type_info.name
