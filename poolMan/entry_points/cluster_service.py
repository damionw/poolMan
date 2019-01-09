#! /usr/bin/env python

#================================================================
#                     Global Imports
#================================================================
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from tornado import ioloop

import logging

#================================================================
#                        Local Imports
#================================================================
from ..options import register_options as pool_options
from ..reactors import MulticastTransponder

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
def run_cluster():
    logging.basicConfig(level=logging.INFO)

    parser = ArgumentParser(
        formatter_class=ArgumentDefaultsHelpFormatter,
        description="Cluster Service",
    )

    pool_options(parser)
    register_options(parser)
    arguments = parser.parse_args()

    ioloop_instance = ioloop.IOLoop.instance()

    transponder = MulticastTransponder(
        group="224.0.0.99",
        port=50500,
        ioloop_instance=ioloop_instance,
    )

    ioloop_instance.start()

#================================================================
#                        Command line startup
#================================================================
if __name__ == "__main__":
   run_cluster()
