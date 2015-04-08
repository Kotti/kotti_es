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


@subscribe(ObjectAfterInsert, Content)
def object_added(event):
    request = event.request
    registry = get_current_registry()
    #registry = request.registry
    wrapped = registry.queryAdapter(event.object, IElastic)
    es_client = get_client(request)
    es_client.index_object(wrapped)


@subscribe(ObjectUpdate, Content)
def object_updated(event):
    import pdb; pdb.set_trace()
    pass


@subscribe(ObjectDelete, Content)
def object_deleted(event):
    import pdb; pdb.set_trace()
    pass
