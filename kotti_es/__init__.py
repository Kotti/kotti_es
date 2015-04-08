# -*- coding: utf-8 -*-

"""
Created on 2015-04-08
:author: Davide Moro (davide.moro@gmail.com)
"""


def kotti_configure(settings):
    """ Add a line like this to you .ini file::

            kotti.configurators =
                kotti_es.kotti_configure

        to enable the ``kotti_es`` add-on.

    :param settings: Kotti configuration dictionary.
    :type settings: dict
    """

    settings['pyramid.includes'] += ' kotti_es'


def includeme(config):
    """ Don't add this to your ``pyramid_includes``, but add the
    ``kotti_configure`` above to your ``kotti.configurators`` instead.

    :param config: Pyramid configurator object.
    :type config: :class:`pyramid.config.Configurator`
    """

    config.include('pyramid_es')

    config.scan(__name__)
