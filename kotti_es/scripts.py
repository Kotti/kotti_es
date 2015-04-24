import optparse
import sys
import textwrap

from pyramid.paster import bootstrap


def reindex_es():
    description = """\
    Reindex ES.  Example:
    'reindex_es -c production.ini'
    """
    usage = "usage: %prog -c config_uri"
    parser = optparse.OptionParser(
        usage=usage,
        description=textwrap.dedent(description)
    )

    parser.add_option(
        '-c', '--config_uri',
        dest='config_uri',
        action='store',
        type='string',
        help=('The config file example: development.ini'),
    )

    options, args = parser.parse_args(sys.argv)

    if options.config_uri:
        try:
            env = bootstrap(options.config_uri)
        except Exception, e:
            print "Can't use the config file %s `%s`" % (options.config_uri, e)
        else:
            # no exceptions, env initialized
            try:
                _reindex_es()
            finally:
                # called env closer
                env['closer']()
    else:
        print 'Config file is required try --help'


def _reindex_es():
    # TODO
    import pdb
    pdb.set_trace()
    pass
