# -*- coding: utf-8 -*-

"""
Created on 2015-04-08
:author: Davide Moro (davide.moro@gmail.com)
"""

from pytest import fixture

pytest_plugins = "kotti"


@fixture(scope='session')
def custom_settings():
    import kotti_es.resources
    kotti_es.resources  # make pyflakes happy
    return {
        'kotti.configurators': 'kotti_tinymce.kotti_configure '
                               'kotti_es.kotti_configure'}
