# -*- coding: utf-8 -*-

"""
Created on 2015-04-08
:author: Davide Moro (davide.moro@gmail.com)
"""

from pytest import fixture

pytest_plugins = "kotti"


@fixture(scope='session')
def custom_settings():
    return {
        'elastic.index': 'kotti_es_test',
        'kotti_es.index_action': 'kotti_es.sqla.default_index_action',
        'kotti_es.is_blacklisted': 'kotti_es.util.is_blacklisted',
        'kotti.configurators': 'kotti_tinymce.kotti_configure '
                               'kotti_es.kotti_configure'}
