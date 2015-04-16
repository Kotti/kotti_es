import sqlalchemy
from sqlalchemy.orm import mapper
from pyramid.threadlocal import (
    get_current_request,
    )

from elasticsearch.exceptions import NotFoundError
from pyramid_es import get_client

from kotti import DBSession
from kotti.interfaces import IContent

_WIRED_SQLALCHEMY = False

INSERT_CODE = 1
DELETE_CODE = -1


def _after_insert(mapper, connection, target):
    request = get_current_request()
    if request:
        if IContent.providedBy(target):
            request._index_list = [(target, INSERT_CODE)]


def _after_delete(mapper, connection, target):
    request = get_current_request()
    if request:
        if IContent.providedBy(target):
            if not hasattr(request, '_index_list'):
                request._index_list = [(target, DELETE_CODE)]
            else:
                request._index_list.append((target, DELETE_CODE))


def _after_commit(session):
    request = get_current_request()
    if request:
        index_list = getattr(request, '_index_list', [])
        es_client = get_client(request)
        for target, operation in index_list:
            if operation == INSERT_CODE:
                es_client.index_object(target, immediate=True)
            elif operation == DELETE_CODE:
                try:
                    es_client.delete_object(target, immediate=True)
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
