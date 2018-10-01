from .constants import DEFAULT_RSA_KEYFILE, DEFAULT_USERNAME
from .decorators import cast, cached

import paramiko # See: https://gist.github.com/ghawkgu/944017
import logging

LOG = logging.getLogger(__name__)

class Host(object):
    def __init__(self, parent, hostname, username=DEFAULT_USERNAME):
        self._parent = parent
        self._hostname = hostname
        self._username = username
        self._client = paramiko.SSHClient()

    def __del__(self):
        self.close()

    @property
    @cached
    def keyfile(self):
        return self._parent._keyfile

    @property
    @cached
    def sshkey(self):
        return paramiko.RSAKey.from_private_key_file(self.keyfile)

    def connect(self):
        self._client.load_system_host_keys()

        return self._client.connect(
            username=self._username,
            hostname="loquat",
            pkey=self.sshkey,
            port=22,
        )

    def close(self):
        self._client.close()

    @property
    def ready(self):
        self.connect()
        _stdin, _stdout, _stderr = self._client.exec_command("ls -l")

        return [
            _row for _row in _stdout
        ]

class Pool(object):
    class _HostLookup(dict):
        def __init__(self, pool, keyfile=DEFAULT_RSA_KEYFILE):
            self._pool = pool
            self._keyfile = keyfile
            super(Pool._HostLookup, self).__init__()

        def __getitem__(self, hostname):
            host = super(Pool._HostLookup, self).get(hostname)

            if host is not None:
                return host

            if hostname not in self._pool._hosts:
                raise KeyError("Unknown or unconfigured pool host {}".format(hostname))

            host = Host(parent=self._pool, hostname=hostname)

            super(Pool._HostLookup, self).__setitem__(hostname, host)

            return host

        def __setitem__(self, hostname, value):
            raise KeyError("Cannot dynamically add pool hosts (yet)")

    def __init__(self, keyfile, hosts=None):
        self._hosts = {} if hosts is None else set(hosts)
        self._keyfile = keyfile
        self._hostlookup = Pool._HostLookup(self)

    @property
    def host(self):
        return self._hostlookup

