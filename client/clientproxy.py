import os, sys, pdb, errno
from utils.helpers import *
from utils.clientconnection import ClientConnection


class ClientProxy(ClientConnection):
    """
    ClientProxy to provide transparency to the client,
    the client only requires the file name/directory of file(later) for reading and writing
    """

    def __init__(self, ds_host, ds_port, ls_host, ls_port):
        super(ClientProxy, self).__init__()
        self.ds_host = ds_host
        self.ds_port = ds_port
        self.ls_host = ls_host
        self.ls_port = ls_port

    def read(self, file_name):
        self.send_as_client(self.ds_host, self.ds_port, get_file_meta(file_name))
        response = str(self.recv(1024))
        if response in response404():
            return response
        response = response.split()
        ip_port = response[2]
        ip_port = ip_port.split(':')
        file_path = response[3]
        file_hash = response[4]
        self.send_as_client(self.ls_host, self.ls_port, check_if_locked(file_name))
        response = str(self.recv(1024))
        pdb.set_trace()
        if response is responseLocked():
            return response
        self.new_connection(ip_port[0], int(ip_port[1]), open_file(file_path+file_hash))
        self.recv_file(file_path, file_name)

    def write(self, file):
        self.send_as_client(self.ds_host, self.ds_port, insert_file_meta(file))
        response = str(self.recv(1024))
        if response in response404():
            return response
        response = response.split()
        ip_port = response[2]
        ip_port = ip_port.split(':')
        file_path = response[3]
        self.send_as_client(self.ls_host, self.ls_port, lock_file(file_path+file))
        response = str(self.recv(1024))
        pdb.set_trace()
        if response is responseLocked():
            return response
        self.new_connection(ip_port[0], int(ip_port[1]), open_file(file_path+file))
        self.send_file(file_path, file)

    def delete(self):
        pass

    def add_directory(self):
        pass

    def delete_directory(self):
        pass

    def _handler(self):
        pass


def main():
    client_proxy = ClientProxy(sys.argv[1], int(sys.argv[2]), sys.argv[3], int(sys.argv[4]))
    client_proxy.read('file.py')



def exit():
    sys.exit(1)


if __name__ == "__main__":
    main()
