import os

from ._version import get_versions
VERSION = get_versions()['version']
del get_versions

API_VERSION = os.environ.get('REN_API_VERSION', 0)

# Logging stuff
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(name)s[%(lineno)s][%(threadName)s] - %(message)s'

LOGLEVEL = 'INFO'
LOGLEVEL = os.environ.get('RI_LOGLEVEL', LOGLEVEL).upper()

CONFIG_PATH = os.environ.get('RI_CONFIG_PATH', os.path.join(os.getcwd(), 'ri.yml'))
if not os.path.isfile(CONFIG_PATH):
    CONFIG_PATH = os.path.join(os.path.expanduser('~'), '.ri.yml')


REMOTE_ADDR = 'https://r.ren-isac.net/api'
REMOTE_ADDR = os.environ.get('REN_REMOTE_ADDR', REMOTE_ADDR)

TOKEN = os.environ.get('REN_TOKEN', None)
FORMAT = os.environ.get('REN_FORMAT', 'table')

TIMEOUT = os.environ.get('REN_TIMEOUT', 300)

