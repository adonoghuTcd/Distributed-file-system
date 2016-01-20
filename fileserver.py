import os, sys, pdb, errno, shutil, socket
from server.server import Server
from utils.helpers import *


class FileService(object):
    """docstring for FileService"""

    def __init__(self, port, ds_host, ds_port):
        super(FileService, self).__init__()
        self.dir = ''
        self.port = port
        self.ds_host = ds_host
        self.ds_port = ds_port
        self.server = Server(port, self._handler)

    def announce_server(self):
        sock = self.server.send_as_client(self.ds_host, self.ds_port, "INSERT " + self.server.host + ":" + str(self.port) + " " + "1")
        data = sock.recv(1024)
        if data.decode('utf-8') != response200():
            print("Error with Directory Server: ", data)
        sock.shutdown(socket.SHUT_WR)
        sock.close()
        #TODO Add to allow exsting files or remove

    def _open_handler(self, conn, path):
        filename = self.dir + path
        if not os.path.isfile(filename):
            self.server.error(conn, 404, response404())
        else:
            f = open(filename, "rb")
            pdb.set_trace()
            self.server.send_file(conn, f)
            conn.shutdown(socket.SHUT_WR)
            conn.close()

    def _create_handler(self, conn, path):
        file_path = os.path.dirname(path)
        if not os.path.isdir(file_path):
            self.server.error(conn, 405, response405())
        else:
            self.server.respond(conn, response200())
            exists = os.path.isfile(self.dir + path)
            f = open(self.dir + path, "wb")
            conn.recv_file(f)
            f.close()
            self.server.respond(conn, response200())
            # TODO: send to other replication managers
            # if not exists:
            #

    def _mkdir_handler(self, conn, path):
        newdir = str(self.dir + path.strip('/'))
        basedir = os.path.dirname(newdir)
        if not os.path.isdir(basedir):
            self.server.error(conn, 404, response404())
        else:
            try:
                os.makedirs(newdir)
                self.server.respond(conn, response200())
                # self._advertise_buffer.add(path.strip('/'), ObjectBuffer.Type.directory)
                # TODO: send to replication manager
            except Exception as e:
                if e.errno != errno.EEXIST:
                    raise
                else:
                    conn.send()

    def _delete_handler(self, conn, path):
        pdb.set_trace()
        obj = str(self.dir + path).rstrip('/')
        if os.path.isdir(obj):
            shutil.rmtree(obj)
            self.server.respond(conn, response200())
            # self._advertise_buffer.add(path, ObjectBuffer.Type.deleteDirectory)
        elif os.path.isfile(obj):
            os.remove(obj)
            self.server.respond(conn, response200())
            # self._advertise_buffer.add(path, ObjectBuffer.Type.deleteFile)
        else:
            self.server.error(conn, 404, "not found!")

    def _handler(self, sock):
        LF = "\n"
        try:
            data = sock.recv(1024)
            msg = data.decode('utf-8')
            msg = msg.replace('$', ' ')
            if 'KILL_SERVICE' in msg:
                exit()
            elif msg[:4] == "HELO":
                response = ["IP:" + self.server.host, "Port:" + str(self.port), "StudentID:" + self.server.studentId]
                fullResponse = msg + LF.join(response)
                print(response)
                sock.send(fullResponse.encode('utf-8'))
            elif msg[:4] == "OPEN":
                temp = msg.split()
                self._open_handler(sock, temp[1])
            elif msg[:6] == "CREATE":
                temp = msg.split()
                self._create_handler(sock, temp[1])
            elif msg[:5] == "MKDIR":
                temp = msg.split()
                self._mkdir_handler(sock, temp[1])
            elif msg[:6] == "DELETE":
                temp = msg.split()
                self._delete_handler(sock, temp[1])
            else:
                self.server.error(sock, 0, responseErrParse())
        except sock.error as e:
            err = e.args[0]
            self.server.error(sock, 0, e.args[1])


def main():
    node = FileService(int(sys.argv[1]),sys.argv[2], int(sys.argv[3]))
    node.announce_server()
    node.server.start()


def exit():
    sys.exit(1)

if __name__ == "__main__":
    main()
