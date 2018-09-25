from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

#================================================================
#                     Option Handling
#================================================================
def register_options(option_parser=None):
    if option_parser is None:
        option_parser = ArgumentParser(
            formatter_class=ArgumentDefaultsHelpFormatter,
        )

    option_parser.add_argument(
        "--host",
        dest="pool_hosts",
        help="Cluster hosts",
        action="append",
        default=[],
    )

    return option_parser
