import logging
import requests
import time
import json
import textwrap
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from ri_registry.constants import VERSION, API_VERSION, TIMEOUT, REMOTE_ADDR, CONFIG_PATH, TOKEN, FORMAT
from ri_registry.exceptions import AuthError, TimeoutError, InvalidSearch, MissingConfig
from ri_registry.utils import setup_logging, get_argument_parser, read_config
from ri_registry.format import FORMATS

from pprint import pprint


class Client(object):

    def __init__(self, remote, token, proxy=None, timeout=TIMEOUT, verify_ssl=True, **kwargs):

        self.logger = logging.getLogger(__name__)
        self.remote = remote
        self.token = str(token)

        self.proxy = proxy
        self.timeout = timeout
        self.verify_ssl = verify_ssl

        self.session = requests.Session()
        self.session.headers["Accept"] = 'application/vnd.r.renisac.v{}+json'.format(API_VERSION)
        self.session.headers['User-Agent'] = 'ri_registry/{}'.format(VERSION)
        self.session.headers['Authorization'] = 'Token token=' + self.token
        self.session.headers['Content-Type'] = 'application/json'

    def _get(self, uri, params={}):
        if not uri.startswith('http'):
            uri = self.remote + uri
        body = self.session.get(uri, params=params, verify=self.verify_ssl)

        if body.status_code > 303:
            err = 'request failed: %s' % str(body.status_code)
            self.logger.debug(err)

            if body.status_code == 401:
                raise AuthError('invalid token')
            elif body.status_code == 404:
                err = 'not found'
                raise RuntimeError(err)
            elif body.status_code == 408:
                raise TimeoutError('timeout')
            else:
                try:
                    err = json.loads(body.content).get('message')
                    raise RuntimeError(err)
                except ValueError as e:
                    err = body.content
                    self.logger.error(err)
                    raise RuntimeError(err)

        return json.loads(body.content)

    def members(self, filters={}):
        rv = self._get('/members', params=filters)
        return rv

    def domains(self, filters={}):
        rv = self._get('/domains', params=filters)
        return rv

    def asns(self, filters={}):
        rv = self._get('asns', params=filters)
        return rv


def main():
    p = get_argument_parser()
    p = ArgumentParser(
        description=textwrap.dedent('''\
        example usage:
            $ ri --members
            $ ri --members -q indiana university
            $ ri --domains
            $ ri --domains -q indiana.edu
            $ ri --prefixes
        '''),
        formatter_class=RawDescriptionHelpFormatter,
        prog='ri',
        parents=[p]
    )
    p.add_argument('--config', help='specify config file [default %(default)s]', default=CONFIG_PATH)
    p.add_argument('--token', help='specify api token [default %(default)s]', default=TOKEN)
    p.add_argument('--remote', help='specify API remote [default %(default)s]', default=REMOTE_ADDR)

    p.add_argument('--members', help='filter for members', action='store_true')
    p.add_argument('--domains', help='filter for domains', action='store_true')
    p.add_argument('--asns', help='filter for asns', action='store_true')
    p.add_argument('-q', help='filter results by q')

    p.add_argument('-f', '--format', help='specify output format [default: %(default)s]', default=FORMAT,
                   choices=FORMATS.keys())


    args = p.parse_args()

    setup_logging(args)
    logger = logging.getLogger(__name__)

    o = {}
    try:
        o = read_config(args)
    except MissingConfig:
        pass

    options = vars(args)
    for v in options:
        if v == 'remote' and options[v] == REMOTE_ADDR and o.get('remote'):
            options[v] = o['remote']
        if options[v] is None:
            options[v] = o.get(v)

    if not options.get('token'):
        raise RuntimeError('missing --token')

    verify_ssl = True
    if o.get('no_verify_ssl') or options.get('no_verify_ssl'):
        verify_ssl = False

    cli = Client(args.remote, args.token, verify_ssl=verify_ssl)

    if args.members:
        search_handler = cli.members

    if args.domains:
        search_handler = cli.domains

    if args.asns:
        search_handler = cli.asns

    try:
        rv = search_handler(filters={'q': args.q})
    except AuthError:
        logger.error('unauthorized')
    except InvalidSearch as e:
        logger.error('invalid search')
    except Exception as e:
        import traceback
        traceback.print_exc()
        logger.error(e)
    else:
        print(FORMATS[options['format']](data=rv))

if __name__ == "__main__":
    main()
