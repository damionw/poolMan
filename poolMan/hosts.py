from .constants import DEFAULT_RSA_KEYFILE, DEFAULT_USERNAME
from .decorators import cast, cached

from collections import namedtuple

import paramiko # See: https://gist.github.com/ghawkgu/944017
import logging

ConnectionState = namedtuple(
    "ConnectionState", [
        "client",
        "channel",
    ]
)

LOG = logging.getLogger(__name__)

class LocalHost(object):
    def __init__(self, pool, hostname):
        self._hostname = hostname
        self._pool = pool

    def _execute(self, command):
        raise Exception("UNFINISHED")
        pass

class Host(object):
    def __init__(self, pool, hostname):
        self._hostname = hostname
        self._pool = pool

    def connection(self):
        class ConnectionWrapper(object):
            def __init__(self, host):
                self._host = host
                self._client = None

            def __enter__(self):
                client = paramiko.SSHClient()
                client.load_system_host_keys()

                client.connect(
                    username=self._host._pool.username,
                    hostname=self._host._hostname,
                    pkey=self._host._pool.ssh_key,
                    port=self._host._pool.ssh_port      ,
                )

                self._client = client

                return client

            def __exit__(self, exception_type, exception_value, traceback):
                client = self._client
                self._client = None
                client.close()

        return ConnectionWrapper(host=self)

    def _execute(self, command):
        def consume(channel):
            while not channel.exit_status_ready():
                if channel.recv_ready():
                    while True:
                        msg = str(stdout.channel.recv(1024))

                        if not len(msg):
                            break

                        yield msg

        with self.connection() as client:
            stdin, stdout, stderr = client.exec_command(command)

            stdout_data = reduce(lambda _x, _y: _x + _y, consume(stdout.channel), "")
            stderr_data = reduce(lambda _x, _y: _x + _y, consume(stderr.channel), "")

            exit_status = stdout.channel.recv_exit_status()

            if exit_status:
                raise Exception(stderr_data)

            return [
                _row.strip() for _row in stdout_data.split("\n")
            ]

    @property
    def available(self):
        try:
            return self._execute("true")
        except BaseException, _exception:
            LOG.warning(repr(_exception))

        return False

    @property
    def test(self):
        return self._execute("false")
