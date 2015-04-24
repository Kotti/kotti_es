kotti_es
********

\This is an extension to Kotti that allows to add `ElasticSearch` (https://www.elastic.co/products/elasticsearch)
support to your site.
It is based on a `pyramid_es` fork (there is a pending PR) and it should be considered still
**experimental**, so use `kotti_es` at your own risk.

|build status|_

`Find out more about Kotti`_

Development happens at https://github.com/davidemoro/kotti_es

.. |build status| image:: https://secure.travis-ci.org/truelab/kotti_es.png?branch=master
.. _build status: http://travis-ci.org/davidemoro/kotti_es
.. _Find out more about Kotti: http://pypi.python.org/pypi/Kotti

Setup
=====

To enable the extension in your Kotti site, activate the configurator::

    kotti.configurators =
        kotti_es.kotti_configure

    elastic.index = mip_project
    elastic.servers = localhost:9200
    elastic.ensure_index_on_start = 1
    kotti_es.blacklist =
        File
        Image
        ...

    kotti.search_content = kotti_es.util.es_search_content

Development
===========

Contributions to kotti_es are highly welcome.
Just clone its `Github repository`_ and submit your contributions as pull requests.

.. _tracker: https://github.com/truelab/kotti_es/issues
.. _Github repository: https://github.com/truelab/kotti_es

Authors
=======

* Davide Moro (@davidemoro)
