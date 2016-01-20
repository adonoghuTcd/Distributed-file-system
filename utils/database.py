import sqlite3, socket, pdb
from utils.helpers import *


class Database:

    def fetch_sql(self, cmd, args):
        conn = sqlite3.connect(DATABASE())
        cur = conn.cursor()
        try:
            cur.execute(cmd, args)
            data = cur.fetchall()
            conn.commit()
            conn.close()
            return data
        except:
            return None

    def execute_sql(self, cmd, args, exclusive=False):
        conn = sqlite3.connect(DATABASE())
        if exclusive:
            conn.isolation_level = 'EXCLUSIVE'
            conn.execute('BEGIN EXCLUSIVE')

        cur = conn.cursor()
        try:
            cur.execute(cmd, args)
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            return False
