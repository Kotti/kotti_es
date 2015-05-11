from lxml.html import document_fromstring
from lxml.html.clean import Cleaner

from pyramid.settings import aslist
from pyramid.threadlocal import (
    get_current_request,
    get_current_registry,
    )
from pyramid.util import DottedNameResolver
from pyramid_es import get_client
from kotti.interfaces import IContent
from kotti import get_settings


def blacklist_from_settings(settings):
    """ Returns a list of type names we don't want to index
    """
    blacklist = []
    raw_blacklist = settings.get('kotti_es.blacklist')
    if raw_blacklist:
        blacklist = aslist(raw_blacklist)
    return blacklist


def get_is_blacklisted():
    """ Returns the is_blacklisted function or the default fallback """
    settings = get_settings()
    is_blacklisted_dotted = settings.get('kotti_es.is_blacklisted')
    is_blacklisted = DottedNameResolver(None).resolve(is_blacklisted_dotted)
    return is_blacklisted


def is_blacklisted(target):
    """ Default function for blacklisting object from indexing.
        You can override this default policy registering
        a ``kotti_es.is_blacklisted`` hook.

        Avoid indexing resources depending on:
        * IContent
        * type name not listed in ``kotti_es.blacklist``
    """
    is_blacklisted = True

    if IContent.providedBy(target):
        request = get_request(target)
        registry = getattr(request, 'registry', None)
        if registry is None:
            registry = get_current_registry()
        settings = registry.settings
        blacklist = blacklist_from_settings(settings)
        type_name = target.type_info.name
        is_blacklisted = type_name in blacklist
    return is_blacklisted


def get_request(target):
    """ Returns the request from the target. If not available
        if will returned the result of the get_current_request
        function.
    """
    request = getattr(target, 'request', None)
    if request is None:
        request = get_current_request()
    return request


_cleaner = Cleaner()
_cleaner.javascript = True
_cleaner.style = True


def html_to_text(value, cleaner=_cleaner):
    """ Returns cleaned html """
    if value:
        cleaned = cleaner.clean_html(value)
        document = document_fromstring(cleaned)
        return document.text_content()
    return ''


def es_search_content(search_term, request=None):
    """ ES search content """
    if not request:
        request = get_current_request()
    client = get_client(request)
    results = client.es.search(client.index, q=search_term)['hits']['hits']
    return [item['_source'] for item in results]
