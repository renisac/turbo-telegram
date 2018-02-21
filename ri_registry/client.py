import logging
import requests
import json
import textwrap
import os
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from ri_registry.constants import VERSION, API_VERSION, TIMEOUT, REMOTE_ADDR, TOKEN
from ri_registry.exceptions import AuthError, NotFound
from ri_registry.utils import setup_logging, get_argument_parser
from ri_registry.format import FORMATS, COLUMNS
from pprint import pprint

TRACE = os.getenv('RI_TRACE', False)

logger = logging.getLogger(__name__)

logger.setLevel(logging.WARNING)
logging.getLogger('requests.packages.urllib3.connectionpool').setLevel(logging.ERROR)

if TRACE:
    logger.setLevel(logging.DEBUG)
    logging.getLogger('requests.packages.urllib3.connectionpool').setLevel(logging.DEBUG)


class Client(object):

    def __init__(self, remote, token, proxy=None, timeout=TIMEOUT, verify_ssl=True, **kwargs):
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
        self.session.headers['Accept-Encoding'] = 'deflate'

    def _check_resp(self, resp, expects=200):

        if isinstance(expects, int):
            expects = [expects]

        if resp.status_code in expects:
            return True

        if resp.status_code in [401, 403]:
            raise AuthError(resp.text)

        if resp.status_code == 404:
            raise NotFound(resp.text)

        raise RuntimeError(resp.text)

    def _get(self, uri, params={}):
        if not uri.startswith('http'):
            uri = self.remote + uri

        resp = self.session.get(uri, params=params, verify=self.verify_ssl)
        self._check_resp(resp, 200)

        return json.loads(resp.text)

    def members(self, filters={}):
        return self._get('/members', params=filters)

    def users(self, filters={}):
        return self._get('/users', params=filters)


def main():
    p = get_argument_parser()
    p = ArgumentParser(
        description=textwrap.dedent('''\
        Environmental Variables:
            REN_TOKEN

        example usage:
            $ REN_TOKEN=1234 ri --members
            $ ren --members 'indiana university'
            $ ren --users wes
        '''),
        formatter_class=RawDescriptionHelpFormatter,
        prog='ri',
        parents=[p]
    )
    p.add_argument('--token', help='specify api token]', default=TOKEN)
    p.add_argument('--remote', help='specify API remote [default %(default)s]', default=REMOTE_ADDR)

    p.add_argument('--members', help='filter for members')
    p.add_argument('--users', help='filter for users')

    p.add_argument('-f', '--format', help='specify output format [default: %(default)s]', default='table',
                   choices=FORMATS.keys())

    args = p.parse_args()

    setup_logging(args)

    if not args.token:
        raise RuntimeError('missing --token')

    cli = Client(args.remote, args.token)

    cols = COLUMNS

    if args.members:
        rv = cli.members(filters={'q': args.members})

    elif args.users:
        cols = ['username', 'created_at', 'updated_at']
        rv = cli.users(filters={'q': args.users})

    else:
        print("Missing --users or --members flag")
        raise SystemExit

    if args.format == 'raw':
        pprint(rv)
    else:
        for l in FORMATS[args.format].get_lines(rv, cols):
            print(l)


if __name__ == "__main__":
    main()
