import os, sys, pdb, errno, shutil, sqlite3
from server.server import Server
from utils.helpers import *
from utils.database import Database


class DirectoryService(Database):
    DATABASE = "sql.db"

    def __init__(self, port, replication):
        super(DirectoryService, self).__init__()
        self.port = port
        self.replication = replication
        self._create_tables()
        self.server = Server(port, self._handler)

    def _insert_server(self, sock, master, host, port):
        exists = self._server_exists(host, port)
        if exists:
            return True
        else:
            self.execute_sql("insert into servers (master, host, port) values (?, ?, ?)", (master, host, port), exclusive=True)
            return True

    def _delete_server(self, sock, host, port):
        self.execute_sql("delete from servers where host=? and port=?", (host, port))

    def _list_servers(self, sock):
        # return (pickle.dumps(self.fetch_sql("select * from servers", ())), "PADDING")
         pass

    def _server_exists(self, host, port):
        return len(self.fetch_sql("select * from servers where host=? and port=?", (host, port))) != 0

    def _select_random_server(self):
        return self.fetch_sql("select * from servers where id >= (abs(random()) % (SELECT max(id) FROM servers));", ())

    def _select_server_by_id(self, id):
        return self.fetch_sql("select * from servers where id=?", (str(id),))

    def _select_server_master(self, host, port):
        return self.fetch_sql("select id from servers where host=? and port=?", (host, port))

    def _find_directory_host(self, file_name):
        return self.fetch_sql("select * from directories where file=?", (file_name,))

    def _insert_directory_host(self, directory, file_name, server_id):
        self.execute_sql("insert into directories (directory, file, server_id) values (?, ?, ?)",
                         (directory, file_name, str(server_id)))

    def _create_tables(self):
        conn = sqlite3.connect(self.DATABASE)
        cur = conn.cursor()
        cur.executescript("""
                create table if not exists servers(
                    id INTEGER PRIMARY KEY ASC,
                    master INTEGER,
                    host TEXT,
                    port TEXT
                );
                create table if not exists directories(
                    id INTEGER PRIMARY KEY ASC,
                    directory TEXT,
                    file TEXT,
                    server_id TEXT
                );""")

    def _handler(self, sock):
        try:
            data = sock.recv(1024)
            msg = data.decode('utf-8')
            msg = msg.replace('$', ' ')
            if 'KILL_SERVICE' in msg:
                exit()

            elif msg[:6] == "INSERT":
                temp = msg.split()
                ip_port = temp[1].split(':')
                master = temp[2]
                self._insert_server(sock, master, ip_port[0], ip_port[1])
                self.server.respond(sock, response200())

            elif msg[:4] == "DELETE":
                temp = msg.split()
                ip_port = temp[1].split(':')
                self._delete_server(sock, ip_port[0], ip_port[1])
                self.server.respond(sock, response200())

            elif msg[:3] == "GET":
                temp = msg.split()
                file_name = temp[1]
                row = self._select_random_server()
                file_dir = self._find_directory_host(file_name)
                pdb.set_trace()
                if file_dir is not None:
                    response = response200() + " " + row[0][2] + ":" + row[0][3] + " " + file_dir[0][1] + " " + str(file_dir[0][0])
                    self.server.respond(sock, response)
                else:
                    self.server.respond(sock, response404())

            elif msg[:4] == "LIST":
                # TODO not complete, for replication
                temp = msg.split()
                #self._mkdir_handler(sock, temp[1])

            elif msg[:3] == "ADD":
                temp = msg.split()
                ip_port = temp[1].split(':')
                server_ids = self._select_server_master(ip_port[0], ip_port[1])
                server_id = server_ids[0]
                self._insert_directory_host(temp[2], temp[3], server_id[0])
            else:
                self.server.error(sock, 0, responseErrParse())
        except sock.error as e:
            err = e.args[0]
            self.server.error(sock, 0, e.args[1])


def main():
    dir_server = DirectoryService(int(sys.argv[1]), sys.argv[2])
    dir_server.server.start()


def exit():
    sys.exit(1)

if __name__ == "__main__":
    main()
