from zope.interface import implements
from zope.component import (
    adapts,
    )
from kotti.interfaces import (
    IContent,
    )
from pyramid_es.mixin import (
    ESMapping,
    ESString,
    ESField,
    )
from pyramid_es.elastic import ElasticBase
from pyramid_es.interfaces import IElastic
from .util import html_to_text


class BaseElasticKottiContent(ElasticBase):
    implements(IElastic)
    adapts(IContent)

    def elastic_mapping(self):
        """
        This is the base fallback adapter for all contents.

        If exists an ``elastic_mapping`` configuration is available you the
        resource's ``type_info``, it will returned as it is.

        Otherwise, a very basic default mapping is returned (just ``title`` and
        ``description``).

        You can add a ``filter`` keyword argument to the ``ESString``
        properties passing a callable that accepts the value to be
        filtered/changed. For example you could pass a filter=html_to_text
        to a ``body`` property.
        """
        context = self.context
        elastic_mapping = getattr(context.type_info, 'elastic_mapping', None)
        if elastic_mapping is not None:
            return elastic_mapping
        else:
            return ESMapping(
                analyzer='content',
                properties=ESMapping(
                    ESField('_id'),
                    ESString('title', attr='_title'),
                    ESString('description', attr='_description'),
                    ESString('body', attr='_body', filter=html_to_text),
                    ))

    def elastic_document_type(self):
        """
        The elastic document type
        """
        return self.context.type_info.name

    def elastic_document_id(self):
        """
        The elastic document id
        """
        return self.context.id

    # Attr private methods
    @property
    def _id(self):
        return self.elastic_document_id()

    @property
    def _title(self):
        return self.context.title

    @property
    def _description(self):
        return self.context.title

    @property
    def _body(self):
        body = getattr(self.context, 'body', '')
        return body
