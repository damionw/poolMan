from .constants import (
    DEFAULT_RSA_KEYFILE,
    DEFAULT_USERNAME,
    DEFAULT_CLUSTER_HOSTS,
    DEFAULT_SSH_PORT,
)

from .decorators import cast, cached
from .hosts import Host

import paramiko
import logging

LOG = logging.getLogger(__name__)

class Pool(object):
    def __init__(self, keyfile, hostnames=None, username=DEFAULT_USERNAME, ssh_port=DEFAULT_SSH_PORT):
        self._hostnames = {"localhost"} if hostnames is None else set(hostnames)
        self._ssh_keyfile = keyfile
        self._username = username
        self._ssh_port = ssh_port

    @property
    def username(self):
        return self._username

    @property
    def hostnames(self):
        return self._hostnames

    @property
    def ssh_keyfile(self):
        return self._ssh_keyfile

    @property
    def ssh_port(self):
        return self._ssh_port

    @property
    @cached
    def ssh_key(self):
        return paramiko.RSAKey.from_private_key_file(self.ssh_keyfile)

    @property
    @cached
    def host(self):
        class _Proxy(dict):
            def __init__(self, pool):
                self._pool = pool
                super(_Proxy, self).__init__()

            def __getitem__(self, hostname):
                host = super(_Proxy, self).get(hostname)

                if host is not None:
                    return host

                if hostname not in self._pool._hostnames:
                    raise KeyError("Unknown or unconfigured pool host {}".format(hostname))

                host = Host(pool=self._pool, hostname=hostname)

                super(_Proxy, self).__setitem__(hostname, host)

                return host

            def __setitem__(self, hostname, value):
                raise KeyError("Cannot dynamically add pool hosts (yet)")

        return _Proxy(pool=self)
