from ._version import get_versions
VERSION = get_versions()['version']
del get_versions

import os

API_VERSION = os.getenv('REN_API_VERSION', 0)

# Logging stuff
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(name)s[%(lineno)s][%(threadName)s] - %(message)s'

LOGLEVEL = 'ERROR'
LOGLEVEL = os.getenv('RI_LOGLEVEL', LOGLEVEL).upper()

REMOTE_ADDR = 'https://r.ren-isac.net/api'
REMOTE_ADDR = os.getenv('REN_REMOTE_ADDR', REMOTE_ADDR)

TOKEN = os.getenv('REN_TOKEN', None)
FORMAT = os.getenv('REN_FORMAT', 'table')

TIMEOUT = os.getenv('REN_TIMEOUT', 300)

