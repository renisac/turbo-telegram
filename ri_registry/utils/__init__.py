import pkgutil
import logging
from ri_registry.constants import LOG_FORMAT, LOGLEVEL, VERSION
from argparse import ArgumentParser
from ri_registry.exceptions import MissingConfig
import signal
from . import color

import yaml
import os


def read_config(args):
    options = {}
    if os.path.isfile(args.config):
        f = file(args.config)
        config = yaml.load(f)
        if config.get('client'):
            config = config['client']
        f.close()
        if not config:
            raise MissingConfig("Unable to read {} config file".format(args.config))
        for k in config:
            if not options.get(k):
                options[k] = config[k]
    else:
        raise MissingConfig("Unable to read {} config file".format(args.config))
    return options


def get_argument_parser():
    BasicArgs = ArgumentParser(add_help=False)
    BasicArgs.add_argument('-d', '--debug', dest='debug', action="store_true")
    BasicArgs.add_argument('-V', '--version', action='version', version=VERSION)
    return ArgumentParser(parents=[BasicArgs], add_help=False)


def setup_logging(args):
    loglevel = logging.getLevelName(LOGLEVEL)

    if args.debug:
        loglevel = logging.DEBUG

    console = logging.StreamHandler()
    logging.getLogger('').setLevel(loglevel)
    console.setFormatter(logging.Formatter(LOG_FORMAT))
    logging.getLogger('').addHandler(console)


def setup_signals(name):
    logger = logging.getLogger(__name__)

    def sigterm_handler(_signo, _stack_frame):
        logger.info('SIGTERM Caught for {}, shutting down...'.format(name))
        raise SystemExit

    signal.signal(signal.SIGTERM, sigterm_handler)
