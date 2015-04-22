import sqlalchemy
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    mapper,
    )
from pyramid.threadlocal import (
    get_current_request,
    )

from elasticsearch.exceptions import NotFoundError
from kotti.resources import Content
from pyramid_es import get_client

from kotti import DBSession

from .util import (
    is_blacklisted,
    get_request,
    )

_WIRED_SQLALCHEMY = False

INSERT_CODE = 1
DELETE_CODE = -1


def _after_insert_update(mapper, connection, target):
    if not is_blacklisted(target):
        request = get_request(target)
        if request:
            if not hasattr(request, '_index_list'):
                request._index_list = [(target, INSERT_CODE)]
            else:
                request._index_list.append((target, INSERT_CODE))


def _after_delete(mapper, connection, target):
    if not is_blacklisted(target):
        request = get_request(target)
        if request:
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
            target_id = target.id
            try:
                target.name
            except sqlalchemy.exc.InvalidRequestError:
                session = scoped_session(sessionmaker())
                target = session.query(Content).filter_by(id=target_id).first()
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
    sqlalchemy.event.listen(mapper, 'after_insert', _after_insert_update)
    sqlalchemy.event.listen(mapper, 'after_update', _after_insert_update)
    sqlalchemy.event.listen(mapper, 'after_delete', _after_delete)
    sqlalchemy.event.listen(DBSession, 'after_commit', _after_commit)
