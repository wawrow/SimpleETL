#!/usr/bin/env python3
import argparse
import importlib
import logging
import pkgutil
import threading
from time import sleep

import datagenerator

# log = logging.getLogger(__name__)

emitters = [name for _, name, _ in pkgutil.iter_modules(
    datagenerator.__path__) if name.endswith('_emitter')]
generators = [name for _, name, _ in pkgutil.iter_modules(
    datagenerator.__path__) if name.endswith('_generator')]


def args_parser():
    '''Argument parser for emitter setup'''
    argparser = argparse.ArgumentParser(
        description='Emitter settings',
    )

    argparser.add_argument('-e', '--emitter', type=str, choices=emitters,
                           default=emitters[0],
                           help='Emitter module to use')

    argparser.add_argument('-c', '--emitter-config', nargs=2, action='append',
                           help='Emitter configurations')

    argparser.add_argument('-g', '--generator', type=str, choices=generators,
                           default=generators[0],
                           help='Generator module to use')

    argparser.add_argument('-v', '--verbose', help='increase output verbosity',
                           action='store_true')

    argparser.add_argument('-t', '--throughput', help='increase output verbosity',
                           type=float, default=0.5)

    return argparser


def main(args):
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    emittermodule = importlib.import_module("datagenerator." + args.emitter)
    generatormodule = importlib.import_module(
        "datagenerator." + args.generator)
    emitter = emittermodule.Emitter(args.emitter_config)
    waittime = 1 / args.throughput
    while True:
        threading.Thread(target=emitter.send_message, args=(
            generatormodule.generate_reading(), )).start()
        sleep(waittime)


if __name__ == '__main__':
    parser = args_parser()
    mappedargs, remaining = parser.parse_known_args()
    mappedargs.emitter_config = {k: v for k, v in mappedargs.emitter_config}
    main(mappedargs)
