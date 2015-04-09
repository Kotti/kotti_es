import sqlalchemy
from sqlalchemy.orm import mapper
from pyramid.threadlocal import (
    get_current_request,
    get_current_registry,
    )

from pyramid_es import get_client

from kotti.events import (
    notify,
    ObjectEvent,
    ObjectDelete,
    ObjectUpdate,
    subscribe,
    )
from kotti.resources import (
    Content,
    )
from .interfaces import IElastic

_WIRED_SQLALCHEMY = False


class ObjectAfterInsert(ObjectEvent):
    """ Custom event after insert notified when
        the id is already available
    """


def _after_insert(mapper, connection, target):
    notify(ObjectAfterInsert(target, get_current_request()))


def wire_sqlalchemy():  # pragma: no cover
    global _WIRED_SQLALCHEMY
    if _WIRED_SQLALCHEMY:
        return
    else:
        _WIRED_SQLALCHEMY = True
    sqlalchemy.event.listen(mapper, 'after_insert', _after_insert)


def _get_wrapper_from_event(event):
    registry = get_current_registry()
    wrapper = registry.queryAdapter(event.object, IElastic)
    return wrapper


def _get_client_from_event(event):
    request = event.request
    return get_client(request)


@subscribe(ObjectAfterInsert, Content)
@subscribe(ObjectUpdate, Content)
def object_updated(event):
    wrapper = _get_wrapper_from_event(event)
    es_client = _get_client_from_event(event)
    # TODO: without immediate=True if won't work due to a transaction
    # error. To be fixed ASAP
    es_client.index_object(wrapper, immediate=True)


@subscribe(ObjectDelete, Content)
def object_deleted(event):
    wrapper = _get_wrapper_from_event(event)
    es_client = _get_client_from_event(event)
    es_client.delete_object(wrapper, immediate=True)
