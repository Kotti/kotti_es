import sqlalchemy
from sqlalchemy.orm import mapper

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

from . import ESSession

_WIRED_SQLALCHEMY = False

INSERT_CODE = 1
DELETE_CODE = -1


def _after_insert_update(mapper, connection, target):
    if not is_blacklisted(target):
        request = get_request(target)
        if request:
            target_id = target.id
            if not hasattr(request, '_index_list'):
                request._index_list = [(target, target_id, INSERT_CODE)]
            else:
                request._index_list.append((target, target_id, INSERT_CODE))


def _after_delete(mapper, connection, target):
    if not is_blacklisted(target):
        request = get_request(target)
        if request:
            target_id = target.id
            if not hasattr(request, '_index_list'):
                request._index_list = [(target, target_id, DELETE_CODE)]
            else:
                request._index_list.append((target, target_id, DELETE_CODE))


def _after_commit(session):
    request = get_current_request()
    settings = get_settings()
    index_action_dotted = settings['kotti_es.index_action']
    index_action = DottedNameResolver(None).resolve(
        index_action_dotted
        )
    if request:
        # use a global alternative session (the session bound to
        # this hook might be not usable)
        index_action(request)


def default_index_action(request):
    def get_target_by_id(target_id):
        return ESSession.query(Content).filter_by(id=target_id).first()

    def update_target(es_client, target, operation):
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
            es_client = get_client(request)
            for target, target_id, operation in index_list:
                update_target(es_client, target, operation)


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
