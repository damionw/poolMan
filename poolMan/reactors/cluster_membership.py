from tornado import ioloop

import socket
import struct
import errno

class MulticastTransponder(object):
    def __init__(self, group="224.0.0.99", port=50500, ioloop_instance=None):
        self._group = socket.inet_aton(group)
        self._port = port
        self._ioloop = ioloop_instance or ioloop.IOLoop.current()

        self._sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM
        )

        self._sock.settimeout(3)
        self._sock.bind(('', self._port))
        self._sock.setblocking(0)

        multicast_request = struct.pack(
            '4sL',
            self._group,
            socket.INADDR_ANY,
        )

        self._sock.setsockopt(
            socket.IPPROTO_IP,
            socket.IP_ADD_MEMBERSHIP,
            multicast_request,
        )

        self._socket_lookup = {
            self._sock.fileno(): self._sock,
        }

        self._ioloop.add_handler(
            self._sock,
            lambda *args, **kwargs: self.read_event(*args, **kwargs),
            self._ioloop.READ,
        )

    def read_event(self, fd, events):
        while True:
            try:
                data, address = self._sock.recvfrom(1024)
                print "{} from {}".format(data, address)
            except socket.error as e:
                if e.errno in (errno.EWOULDBLOCK, errno.EAGAIN):
                    return
                raise
