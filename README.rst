kotti_es
********

\This is an extension to Kotti that allows to add `ElasticSearch` (https://www.elastic.co/products/elasticsearch)
support to your site.
It is based on a `pyramid_es` fork (there is a pending PR, code available here https://github.com/truelab/pyramid_es/tree/feature-wrapper)
and it should be considered still **experimental**, so use `kotti_es` at your own risk.

|build status|_

`Find out more about Kotti`_

Development happens at https://github.com/Kotti/kotti_es

.. |build status| image:: https://secure.travis-ci.org/Kotti/kotti_es.png?branch=master
.. _build status: http://travis-ci.org/Kotti/kotti_es
.. _Find out more about Kotti: http://pypi.python.org/pypi/Kotti

What is the kotti_es role
=========================

Once enabled ``kotti_es``:

1- implements fulltext search based on ElasticSearch (external service)
   It overrides the default ``kotti.search_content`` hook, this way search results will come from ElasticSearch instead of traditional
   fulltext database searches

2- registers event handlers for insert, update and delete and index contents against ElasticSearch. This way
   when needed ElasticSearch will be updated automatically

3- let you index against ElasticSearch already existing contents before you installed ``kotti_es``. See ``reindex_es`` console script.

4- provides a default common indexer adapter (``kotti_es.elastic.BaseElasticKottiContent``) that extracts data
   for ElasticSearch. You can overide it or register more specific indexer adapters for other content types
   using marker interfaces

5- provides various configuration hooks (custom index actions, override the Kotti's default fulltext search method or not,
   type names blacklist if you want to omit certain types to be indexed, etc)

Setup
=====

Mandatory settings (configurator, index name and servers)::

    kotti.configurators =
        kotti_es.kotti_configure

    elastic.index = mip_project
    elastic.servers = localhost:9200

Optional settings::

    # **elastic.ensure_index_on_start**: connect and create index on start if it does not exist (default: 0)
    elastic.ensure_index_on_start = 1

    # **kotti_es.override_search_content**: if true kotti_es overrides the ``kotti.search_content`` (default: true),
    # so search results come from ElasticSearch by default. In this case the kotti.search_content will be changed
    # to ``kotti_es.util.es_search_content`` by default.
    # If you want you can turn this option fo ``false`` and the default
    # kotti.search_content will be used (performing a traditional fulltext against relational database)
    kotti_es.override_search_content = false    # kotti_es overrides the ``kotti.search_content`` (default: true),

    # **kotti_es.blacklist**: does not index against ElasticSearch type names listed here (default: empty list)
    kotti_es.blacklist =
        File
        Image
        ...

    # **kotti_es.index_action**: you can override the default index_action provided by kotti_es
    # (default: ``kotti_es.sqla.default_index_action``).
    # If you want you can configure a different index action and maybe implement an asynchronous indexing handler
    # kotti_es.index_action = yourcustom.indexaction


You can add ``kotti_es`` to an existing Kotti site and launch the ``reindex_es`` console script::

    $ reindex_es -c app.ini

Development
===========

Contributions to kotti_es are highly welcome.
Just clone its `Github repository`_ and submit your contributions as pull requests.

.. _tracker: https://github.com/truelab/kotti_es/issues
.. _Github repository: https://github.com/truelab/kotti_es

Funding
=======

Developed with the support of:

* MIP (International Business School of Politecnico di Milano) - http://www.mip.polimi.it

Authors
=======

* Davide Moro (https://github.com/davidemoro)
