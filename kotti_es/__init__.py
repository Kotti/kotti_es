# -*- coding: utf-8 -*-

"""
Created on 2015-04-08
:author: Davide Moro (davide.moro@gmail.com)
"""

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )
from pyramid.settings import asbool

ESSession = scoped_session(sessionmaker())


def kotti_configure(settings):
    """ Add a line like this to you .ini file::

            kotti.configurators =
                kotti_es.kotti_configure

        to enable the ``kotti_es`` add-on.

    :param settings: Kotti configuration dictionary.
    :type settings: dict
    """

    settings['pyramid.includes'] += ' kotti_es'
    override_search = asbool(settings.get('kotti_es.override_search_content',
                             True))
    if override_search:
        settings['kotti.search_content'] = 'kotti_es.util.es_search_content'
    if 'kotti_es.index_action' not in settings:
        settings['kotti_es.index_action'] = 'kotti_es.sqla.default_index_action'
    if 'kotti_es.is_blacklisted' not in settings:
        settings['kotti_es.is_blacklisted'] = 'kotti_es.util.is_blacklisted'


def includeme(config):
    """ Don't add this to your ``pyramid_includes``, but add the
    ``kotti_configure`` above to your ``kotti.configurators`` instead.

    :param config: Pyramid configurator object.
    :type config: :class:`pyramid.config.Configurator`
    """

    config.include('pyramid_es')
    config.include('pyramid_zcml')
    config.load_zcml('configure.zcml')

    from .sqla import wire_sqlalchemy
    wire_sqlalchemy()

    config.scan(__name__)
