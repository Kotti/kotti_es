import sqlalchemy
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    mapper,
    )
from pyramid.threadlocal import (
    get_current_request,
    )
from pyramid.util import DottedNameResolver

from elasticsearch.exceptions import NotFoundError
from pyramid_es import get_client

from kotti.resources import Content
from kotti import (
    DBSession,
    get_settings,
    )

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
            target_id = target.id
            if not hasattr(request, '_index_list'):
                request._index_list = [(target_id, INSERT_CODE)]
            else:
                request._index_list.append((target_id, INSERT_CODE))


def _after_delete(mapper, connection, target):
    if not is_blacklisted(target):
        request = get_request(target)
        if request:
            target_id = target.id
            if not hasattr(request, '_index_list'):
                request._index_list = [(target_id, DELETE_CODE)]
            else:
                request._index_list.append((target_id, DELETE_CODE))


def _after_commit(session):
    request = get_current_request()
    settings = get_settings()
    index_action_dotted = settings['kotti_es.index_action']
    index_action = DottedNameResolver(None).resolve(
        index_action_dotted
        )
    if request:
        index_action(session, request)


def default_index_action(session, request):
    def get_target_by_id(session, target_id):
        return session.query(Content).filter_by(id=target_id).one()

    def update_target(session, es_client, target, operation):
        target = session.query(Content).filter_by(id=target.id).one()
        if operation == INSERT_CODE:
            es_client.index_object(target, immediate=True)
        elif operation == DELETE_CODE:
            try:
                es_client.delete_object(target, immediate=True)
            except NotFoundError:
                pass
    request = get_current_request()
    if request:
        index_list = getattr(request, '_index_list', [])
        if index_list:
            new_session = False
            es_client = get_client(request)
            target_id = index_list[0][0]
            operation = index_list[0][1]
            try:
                target = get_target_by_id(session, target_id)
            except sqlalchemy.exc.InvalidRequestError:
                # if you call the @@rename view and you
                # try to change name, you'll get an error
                # because the session is no more usable.
                # Code review will be very appreciated
                new_session = True
                session = scoped_session(sessionmaker())
                target = get_target_by_id(session, target_id)
            update_target(session, es_client, target, operation)
            for target_id, operation in index_list[1:]:
                target = get_target_by_id(session, target_id)
                update_target(session, es_client, target, operation)
            if new_session:
                session.close()


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
