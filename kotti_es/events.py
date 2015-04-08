import sqlalchemy
from sqlalchemy.orm import mapper
from pyramid.threadlocal import get_current_request

from kotti.events import (
    notify,
    ObjectEvent,
    ObjectDelete,
    ObjectUpdate,
    subscribe,
    )
from kotti.interfaces import (
    IContent,
    )

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


@subscribe(ObjectAfterInsert, IContent)
def object_added(event):
    import pdb; pdb.set_trace()
    pass


@subscribe(ObjectUpdate, IContent)
def object_updated(event):
    import pdb; pdb.set_trace()
    pass


@subscribe(ObjectDelete, IContent)
def object_deleted(event):
    import pdb; pdb.set_trace()
    pass
