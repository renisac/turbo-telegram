import textwrap
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from ri_registry.constants import REMOTE_ADDR, CONFIG_PATH, TOKEN
from ri_registry.utils import setup_logging, get_argument_parser
from ri_registry.client import Client

from pprint import pprint


def main():
    p = get_argument_parser()
    p = ArgumentParser(
        description=textwrap.dedent('''\
        Environmental Variables:
            REN_TOKEN
            REN_REMOTE_ADDR

        example usage:
            $ REN_TOKEN=1234 ren-networks
        '''),
        formatter_class=RawDescriptionHelpFormatter,
        prog='ri',
        parents=[p]
    )
    p.add_argument('--config', help='specify config file [default %(default)s]', default=CONFIG_PATH)
    p.add_argument('--token', help='specify api token [default %(default)s]', default=TOKEN)
    p.add_argument('--remote', help='specify API remote [default %(default)s]', default=REMOTE_ADDR)
    p.add_argument('--file', default='contacts.csv')

    args = p.parse_args()

    setup_logging(args)

    cli = Client(args.remote, args.token)

    count = 0
    with open(args.file) as f:
        for l in f.readlines():
            l = l.strip("\n")
            name, netname, domain, www, abuse1, abuse2, prefix, misc1, misc2, misc3 = l.split(';')

            n = {
                'network': {
                    'name': name,
                    'netname': netname,
                    'domain': domain,
                    'abuse1': abuse1,
                    'abuse2': abuse2,
                    'prefix': prefix
                }
            }

            r = cli._post('/networks', n)
            if r:
                count += 1
            else:
                raise RuntimeError()

            if count % 100 == 0:
                print('{} complete...'.format(count))

    print('{} entries sent...'.format(count))

if __name__ == "__main__":
    main()
