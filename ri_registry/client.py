import logging
import requests
import time
import json
import textwrap
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from ri_registry.constants import VERSION, API_VERSION, TIMEOUT, REMOTE_ADDR, CONFIG_PATH, TOKEN, FORMAT
from ri_registry.exceptions import AuthError, TimeoutError, InvalidSearch, MissingConfig, NotFound
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
        self.session.headers['User-Agent'] = 'ri-registry/{}'.format(VERSION)
        self.session.headers['Authorization'] = 'Token token=' + self.token
        self.session.headers['Content-Type'] = 'application/json'

    def _check_resp(self, resp, expects=200):
        if isinstance(expects, int):
            expects = [expects]

        if resp.status_code in expects:
            return True

        if resp.status_code == 401:
            raise AuthError()

        if resp.status_code == 404:
            raise NotFound()

        raise RuntimeError(resp.text)

    def _post(self, uri, data):
        if not uri.startswith('http'):
            uri = self.remote + uri

        data = json.dumps(data)
        resp = self.session.post(uri, data=data, verify=self.verify_ssl)
        self._check_resp(resp, [200, 201])

        return json.loads(resp.text)

    def _get(self, uri, params={}):
        if not uri.startswith('http'):
            uri = self.remote + uri

        resp = self.session.get(uri, params=params, verify=self.verify_ssl)
        self._check_resp(resp, 200)

        return json.loads(resp.text)

    def members(self, filters={}):
        rv = self._get('/members', params=filters)
        return rv

    def organizations(self, filters={}):
        return self._get('/organizations', params=filters)

    def prefixes(self, filters={}):
        return self._get('/prefixes', params=filters)

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
        Environmental Variables:
            REN_TOKEN
            REN_REMOTE_ADDR

        example usage:
            $ REN_TOKEN=1234 ri --members
            $ ren --members -q indiana university
            $ ren --domains
            $ ren --domains -q indiana.edu
            $ ren --prefixes
            $ ren --prefixes -q 129.79.78.188
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
    p.add_argument('--prefixes', help='filter for prefixes', action='store_true')

    p.add_argument('-q', help='filter results by q')

    p.add_argument('-f', '--format', help='specify output format [default: %(default)s]', default='raw',
                   choices=FORMATS.keys())

    args = p.parse_args()

    setup_logging(args)

    if not args.token:
        raise RuntimeError('missing --token')

    cli = Client(args.remote, args.token)

    if args.members:
        search_handler = cli.members

    if args.domains:
        search_handler = cli.domains

    if args.asns:
        search_handler = cli.asns

    if args.prefixes:
        search_handler = cli.prefixes

    rv = search_handler(filters={'q': args.q})

    if args.format == 'raw':
        pprint(rv)
    else:
        for l in FORMATS[args.format].get_lines(rv):
            print(l)

if __name__ == "__main__":
    main()
