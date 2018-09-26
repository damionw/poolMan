from .constants import DEFAULT_CLUSTER_HOSTS

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, Action

#================================================================
#                     Option Handling
#================================================================
class OverrideableListAction(Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        super(OverrideableListAction, self).__init__(option_strings, dest, **kwargs)
        self._initialized = False

    def __call__(self, parser, namespace, values, option_string=None):
        if not self._initialized:
            setattr(namespace, self.dest, {values})
        else:
            getattr(namespace, self.dest).add(values)

        self._initialized = True

def register_options(option_parser=None):
    if option_parser is None:
        option_parser = ArgumentParser(
            formatter_class=ArgumentDefaultsHelpFormatter,
        )

    option_parser.add_argument(
        "--host",
        dest="pool_hosts",
        help="Cluster hosts",
        action=OverrideableListAction,
        default=DEFAULT_CLUSTER_HOSTS,
    )

    return option_parser
