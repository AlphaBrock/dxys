# coding:utf-8

# database connection

import sqlite3

from config import DB_PATH


class Database:

    def __init__(self):
        self.con = sqlite3.connect(DB_PATH, check_same_thread=False)
        self.init_db()

    def __del__(self):
        self.con.close()

    def init_db(self):
        cur = self.con.cursor()
        sub_list = '''CREATE TABLE IF NOT EXISTS sub_list
    (
      id         INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
      chat_id    VARCHAR(20),
      region       VARCHAR(20),
      date TIMESTAMP NOT NULL DEFAULT (datetime('now','localtime'))
    )
        '''
        cur.execute(sub_list)
        self.con.commit()

    def run_query(self, cmd, param=None):
        cur = self.con.cursor()
        if param is None:
            cur.execute(cmd)
        else:
            cur.execute(cmd, param)
        result, count = cur.fetchall(), cur.rowcount
        self.con.commit()
        self.con.close()
        return result, count

    def create_chat_id(self, param):
        sql_cmd = "INSERT INTO sub_list(chat_id, region) VALUES (?,?)"
        self.run_query(sql_cmd, param)

    def query_chat_id(self):
        sql_cmd = "SELECT * FROM sub_list"
        data, _ = self.run_query(sql_cmd)
        return data

    def delete_chat_id(self, param):
        sql_cmd = "DELETE FROM sub_list WHERE chat_id=?"
        _, count = self.run_query(sql_cmd, (param,))
        return count


if __name__ == '__main__':
    Database().init_db()
