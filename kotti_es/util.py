from pyramid.settings import aslist
from pyramid.threadlocal import (
    get_current_request,
    get_current_registry,
    )
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
        request = get_request()
        registry = getattr(request, 'registry')
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
    request = getattr(target, 'request')
    if request is None:
        request = get_current_request()
    return request
