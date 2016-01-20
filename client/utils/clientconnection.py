import socket, pdb, errno, os
from utils.helpers import *


class ClientConnection:

    def new_connection(self, host, port, data):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self._sock.connect((host, port))
            self.send(data.encode('utf-8'))
        except OSError as e:
            if e.errno == errno.ECONNREFUSED:
                print("Connection refused at the address ", host, port)

    def send_as_client(self, remote_host, remote_port, msg):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self._sock.connect((remote_host, remote_port))
            self._sock.send(msg.encode('utf-8'))
        except OSError  as e:
            if e.errno == errno.ECONNREFUSED:
                print("Connection refused at the address ", remote_host, remote_port)

    def send(self, data):
        self._sock.send(data)

    def send_file(self, file):
        f = open(file, "rb")
        l = f.read(1024)
        while l:
            self._sock.send(l)
            l = f.read(1024)

    def recv_file(self, file_path, file_name):
        #if not os.path.exists(file_path):
        #    os.makedirs(file_path)
        f = open(file_path + file_name, 'w')
        l = self._sock.recv(1024).decode('utf-8')
        while l:
            f.write(l)
            l = self._sock.recv(1024).decode('utf-8')
        self._sock.shutdown(socket.SHUT_WR)
        self._sock.close()

    def recv(self, size=-1):
        if size is not -1:
            return self._sock.recv(size).decode('utf-8')
        l = self._sock.recv(1024).decode('utf-8')
        while l:
            l = self._sock.recv(1024).decode('utf-8')
        return l

    def close(self):
        self._sock.close()

    def shutdown(self, method):
        self._sock.shutdown(method)