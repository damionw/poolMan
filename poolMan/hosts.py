from .constants import DEFAULT_RSA_KEYFILE, DEFAULT_USERNAME
from .decorators import cast, cached

import paramiko # See: https://gist.github.com/ghawkgu/944017
import logging

LOG = logging.getLogger(__name__)

class Host(object):
    def __init__(self, pool, hostname):
        self._hostname = hostname
        self._pool = pool

    def connection(self):
        class ConnectionWrapper(object):
            def __init__(self, host):
                self._host = host

            def __enter__(self):
                self._client = paramiko.SSHClient()
                self._client.load_system_host_keys()

                self._client.connect(
                    username=self._host._pool.username,
                    hostname=self._host._hostname,
                    pkey=self._host._pool.ssh_key,
                    port=self._host._pool.ssh_port      ,
                )

                return self._client

            def __exit__(self, exception_type, exception_value, traceback):
                self._client.close()
                self._client = None

        return ConnectionWrapper(host=self)

    def _execute(self, command):
        with self.connection() as client:
            _stdin, _stdout, _stderr = client.exec_command(command)

            return [
                _row.strip() for _row in _stdout
            ]

    @property
    def test(self):
        return self._execute("ls -1")
