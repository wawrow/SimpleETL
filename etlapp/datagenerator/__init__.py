import argparse
import importlib
import logging
import pkgutil
import threading
from time import sleep

from .. import config, datagenerator

# log = logging.getLogger(__name__)
logging.basicConfig(level=config.LOG_LEVEL)

emitters = [__package__ + '.' + name for _, name, _ in pkgutil.iter_modules(
    datagenerator.__path__) if name.endswith('_emitter')]
generators = [__package__ + '.' + name for _, name, _ in pkgutil.iter_modules(
    datagenerator.__path__) if name.endswith('_generator')]


def args_parser():
    '''Argument parser for emitter setup'''
    argparser = argparse.ArgumentParser(
        description='Emitter settings',
    )

    argparser.add_argument('-e', '--emitter', type=str, choices=emitters,
                           default=config.DATA_EMITTER,
                           help='Emitter module to use')

    argparser.add_argument('-c', '--emitter-config', nargs=2, action='append',
                           help='Emitter configurations entry, Example: Url http://localhost')

    argparser.add_argument('-g', '--generator', type=str, choices=generators,
                           default=config.DATA_GENERATOR,
                           help='Generator module to use')

    argparser.add_argument('-v', '--verbose', help='increase output verbosity',
                           action='store_true')

    argparser.add_argument('-t', '--throughput', help='increase output verbosity',
                           type=float, default=config.EMITTER_REQUESTS_PER_SECOND)

    return argparser


def main():

    parser = args_parser()
    args, remaining = parser.parse_known_args()
    args.emitter_config = {
        k: v for k, v in args.emitter_config} if args.emitter_config else {}

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    emittermodule = importlib.import_module(args.emitter)
    generatormodule = importlib.import_module(args.generator)
    emitter = emittermodule.Emitter(args.emitter_config)
    waittime = 1 / args.throughput
    while True:
        threading.Thread(target=emitter.send_message, args=(
            generatormodule.generate_reading(), )).start()
        sleep(waittime)


if __name__ == '__main__':
    main()
