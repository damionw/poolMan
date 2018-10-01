#! /usr/bin/env python

#================================================================
#                     Global Imports
#================================================================
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from os.path import dirname, abspath, expanduser, exists, basename, join
from os import environ
from atexit import register
from readline import read_history_file

import readline
import rlcompleter

localpath = dirname(dirname(dirname(abspath(__file__))))

if exists(join(localpath, 'poolMan', '__init__.py')):
    import sys
    sys.path[:0] = [localpath]

#================================================================
#                      History Facilitation
#================================================================
historyPath = "%s/.poolman_history" % environ['HOME']

def save_history(historyPath=historyPath):
    import readline
    readline.write_history_file(historyPath)

if exists(historyPath):
    read_history_file(historyPath)

register(save_history)

del read_history_file, register, readline, rlcompleter, save_history, historyPath

#================================================================
#                     Option Handling
#================================================================
def register_options(option_parser=None):
    if option_parser is None:
        option_parser = ArgumentParser(
            formatter_class=ArgumentDefaultsHelpFormatter,
            description="Pool Manager Console",
        )

    return option_parser

#================================================================
#                               Main
#================================================================
def console():
    import poolMan
    import logging
    import code

    logging.basicConfig(level=logging.INFO)

    parser = ArgumentParser(
        formatter_class=ArgumentDefaultsHelpFormatter,
        description="Pool Manager Console",
    )

    poolMan.register_options(parser)
    register_options(parser)
    arguments = parser.parse_args()

    pool = poolMan.Pool(
        hostnames=arguments.pool_hosts,
        keyfile=arguments.keyfile,
    )

    code.interact(
        local=dict(globals().items() + locals().items())
    )

#================================================================
#                      Entry Point
#================================================================
if __name__ == "__main__":
    try:
        console()
    except (KeyboardInterrupt):
        exit(0)
