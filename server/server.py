from socket import AF_INET, SOCK_STREAM, gethostname, gethostbyname, socket
from select import select
from concurrent.futures import ThreadPoolExecutor
import sys, pdb, time, threading, errno
from server.messages import *


class Server:
    """
    Base server that implements thread pooling. Server does not handle connection processing, instead callback handlers
    may be passed in on initialisation.
    """
    def __init__(self, port, callback):
        self.studentId = "aa2d8671e0b9698d706dd81e9fdf63205dcaa89b2926e5df2ec7a594b66861ba"
        self.port = port
        self.callback = callback
        self.host = gethostname()#gethostbyname(gethostname())
        self.connections = []
    
    def send_file(self, sock, f):
        l = f.read(1024).decode('utf-8')
        while l:
            sock.send(l.encode('utf-8'))
            l = f.read(1024).decode('utf-8')
        f.close()

    def send_as_client(self, remote_host, remote_port, msg):
        sock = socket(AF_INET, SOCK_STREAM)
        try:
            sock.connect((remote_host, remote_port))
            sock.send(msg.encode('utf-8'))
        except sock.error as e:
            if e.errno == errno.ECONNREFUSED:
                print("Connection refused at the address ", remote_host, remote_port)

        return sock

    def respond(self, sock, msg):
        if sock is not None:
            sock.send(msg.encode('utf-8'))

    def error(self, conn, code, description):
        print("Error %d: %s" % (code, description))
        message = ERROR_MESSAGE.format(
            code=code,
            description=description
        )
        conn.send(message.encode('utf-8'))

    def _new_connection(self):
        client_sock, client_addr = self.sock.accept()
        self.pool.submit(self.callback, client_sock)

    def start(self):
        self.pool = ThreadPoolExecutor(8)
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(8)
        while True:
            try:
                read_sockets, write_sockets, error_sockets = select((self.connections + [self.sock]), [], [])
                for sock in read_sockets:
                    if sock is self.sock:
                        self._new_connection()
                    else:
                        self.pool.submit(self.callback, sock)
            except Exception as e:
                raise


def exit():
    sys.exit(1)


