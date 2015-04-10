import sqlalchemy
from sqlalchemy.orm import mapper
from pyramid.threadlocal import (
    get_current_request,
    get_current_registry,
    )

from elasticsearch.exceptions import NotFoundError
from pyramid_es import get_client

from kotti import DBSession
from kotti.interfaces import IContent
from .interfaces import IElastic

_WIRED_SQLALCHEMY = False


def _after_insert(mapper, connection, target):
    request = get_current_request()
    if IContent.providedBy(target):
        request._index_list = [(target, 1)]


def _after_delete(mapper, connection, target):
    request = get_current_request()
    if IContent.providedBy(target):
        request._index_list = [(target, -1)]


def _after_commit(session):
    request = get_current_request()
    index_list = getattr(request, '_index_list', [])
    registry = get_current_registry()
    es_client = get_client(request)
    for target, operation in index_list:
        wrapper = registry.queryAdapter(target, IElastic)
        if operation == 1:
            es_client.index_object(wrapper, immediate=True)
        else:
            try:
                es_client.delete_object(wrapper, immediate=True)
            except NotFoundError:
                pass


def wire_sqlalchemy():  # pragma: no cover
    global _WIRED_SQLALCHEMY
    if _WIRED_SQLALCHEMY:
        return
    else:
        _WIRED_SQLALCHEMY = True
    sqlalchemy.event.listen(mapper, 'after_insert', _after_insert)
    sqlalchemy.event.listen(mapper, 'after_update', _after_insert)
    sqlalchemy.event.listen(mapper, 'after_delete', _after_delete)
    sqlalchemy.event.listen(DBSession, 'after_commit', _after_commit)
