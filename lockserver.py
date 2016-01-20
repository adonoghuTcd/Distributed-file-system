import os, sys, pdb, errno,shutil, sqlite3, threading
from server.server import Server
from utils.helpers import *
from utils.database import Database


class LockService(Database):
    """
    LockService provdes functionality to lock access to a particular file on the fileservers. 
    Every service that writes to file uses the lockService, every read of a file checks if the particular file is locked.
    The lockservice provides rudimentary acknowledgments on all operations
    """

    DATABASE = "sql.db"
   
    def __init__(self, port):
        super(LockService, self).__init__()
        self.port = port
        self._create_tables()
        self.server = Server(port, self._handler)

    def _lock_file(self, file_name):
        is_locked = self._check_if_locked(file_name)
        if is_locked:
            return False
        insert = self.execute_sql("insert into locks (file_name) values (?)", (file_name,), exclusive=True)
        if insert:
            return True
        else:
            return False

    def _unlock_file(self, file_name):
        delete = self.execute_sql("delete from locks where file_name = ?", (file_name,), exclusive=True)
        if delete:
            return True
        else:
            return False

    def _check_if_locked(self, file_name):
        data = self.fetch_sql("select * from locks where file_name=?", (file_name,))
        if file_name in data:
            return True
        else:
            return False

    def _handler(self, sock):
        try:
            data = sock.recv(1024)
            msg = data.decode('utf-8')
            msg = msg.replace('$', ' ')
            if 'KILL_SERVICE' in msg:
                exit()

            elif msg[:4] == "LOCK":
                temp = msg.split()
                is_locked = self._unlock_file(temp[1])
                if is_locked:
                    self.server.respond(sock, response200())
                else:
                    self.server.respond(sock, response604())

            elif msg[:6] == "UNLOCK":
                temp = msg.split()
                is_unlocked = self._unlock_file( temp[1])
                if is_unlocked:
                    self.server.respond(sock, response200())
                else:
                    self.server.respond(sock, response604())

            elif msg[:5] == "CHECK":
                temp = msg.split()
                locked = self._check_if_locked(temp[1])
                if locked:
                    self.server.respond(sock, responseLocked())
                else:
                    self.server.respond(sock, responseUnlocked())
            else:
                self.server.error(sock, 0, responseErrParse())
        except sock.error as e:
            err = e.args[0]
            self.server.error(sock, 0, e.args[1])

    def _create_tables(self):
        conn = sqlite3.connect(self.DATABASE)
        cur = conn.cursor()
        cur.executescript("""
            create table if not exists locks(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_name TEXT
            );""")


def main():
    dir_server = LockService(int(sys.argv[1]))
    dir_server.server.start()


def exit():
    sys.exit(1)

if __name__ == "__main__":
    main()
