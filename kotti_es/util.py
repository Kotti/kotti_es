from lxml.html import document_fromstring
from lxml.html.clean import Cleaner

from pyramid.settings import aslist
from pyramid.threadlocal import (
    get_current_request,
    get_current_registry,
    )
from pyramid_es import get_client
from kotti.interfaces import IContent


def blacklist_from_settings(settings):
    """ Returns a list of type names we don't want to index
    """
    blacklist = []
    raw_blacklist = settings.get('kotti_es.blacklist')
    if raw_blacklist:
        blacklist = aslist(raw_blacklist)
    return blacklist


def is_blacklisted(target):
    """ Avoid indexing resources depending on:
        * IContent
        * type name not listed in ``kotti_es.blacklist``
    """
    if IContent.providedBy(target):
        request = get_request(target)
        registry = getattr(request, 'registry', None)
        if registry is None:
            registry = get_current_registry()
        settings = registry.settings
        blacklist = blacklist_from_settings(settings)
        type_name = target.type_info.name
        return type_name in blacklist
    return True


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
    # quick and dirty implementation, to be refactored and tested!
    if not request:
        request = get_current_request()
    client = get_client(request)
    results = client.es.search(client.index, q=search_term)['hits']['hits']
    # TODO: index permission principals/localroles/ACL
    return results
