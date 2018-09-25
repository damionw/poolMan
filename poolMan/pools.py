from .decorators import cast

import paramiko # See: https://gist.github.com/ghawkgu/944017
import logging

LOG = logging.getLogger(__name__)

class Pool(object):
    @classmethod
    def from_args(cls, parsed_arguments):
        return cls(
            folder=parsed_arguments.profitloss_path,
        )

    def __init__(self, hosts=None):
        self._hosts = {} if hosts is None else set(hosts)
