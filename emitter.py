#!/usr/bin/env python3
import generator
import generator.rest_emitter
import generator.gaussian_generator
from time import sleep
import logging
import argparse
import pkgutil
import json
import threading

# log = logging.getLogger(__name__)

emitters = [name for _, name, _ in pkgutil.iter_modules(
    generator.__path__) if name.endswith('_emitter')]
generators = [name for _, name, _ in pkgutil.iter_modules(
    generator.__path__) if name.endswith('_generator')]


def args_parser():
    '''Argument parser for emitter setup'''
    parser = argparse.ArgumentParser(
        description='Emitter settings',
    )

    parser.add_argument('-e', '--emitter', type=str, choices=emitters,
                        default=emitters[0],
                        help='Emitter module to use')

    parser.add_argument('-c', '--emitter-config', nargs=2, action='append',
                        help='Emitter configurations')

    parser.add_argument('-g', '--generator', type=str, choices=generators,
                        default=generators[0],
                        help='Generator module to use')

    parser.add_argument('-v', '--verbose', help='increase output verbosity',
                        action='store_true')

    parser.add_argument('-t', '--throughput', help='increase output verbosity',
                        type=float, default=0.5)

    return parser


def main(args=None):
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    emitter = generator.rest_emitter.HttpEmitter(args.emitter_config)
    waittime = 1 / args.throughput
    while True:
        threading.Thread(target=emitter.send_message, args=(
            generator.gaussian_generator.generate_reading(), )).start()
        sleep(waittime)


if __name__ == '__main__':
    parser = args_parser()
    args, remaining = parser.parse_known_args()
    args.emitter_config = {k: v for k, v in args.emitter_config}
    main(args)
