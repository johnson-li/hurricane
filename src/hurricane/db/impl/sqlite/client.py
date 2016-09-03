import logging

import hurricane.db.impl.sqlite

logger = logging.getLogger(__name__)


class Client:
    def __init__(self):
        self.conn = hurricane.db.impl.sqlite.conn

    def db_func_get_user(self, db_filter=None):
        cursor = self.conn.cursor()
        where_clause = 'where {}'.format(str(db_filter)) if db_filter else ''
        sql = 'select * from {} {}'.format('user', where_clause)
        logging.warning(sql)
        cursor.execute(sql)
        users = cursor.fetchall()
        columns = [i[0] for i in cursor.description]
        users = [dict(zip(columns, user)) for user in users]
        return users

    def db_func_update_user(self, update_data, db_filter=None):
        pass

    def db_func_create_user(self, update_data):
        cursor = self.conn.cursor()
        keys = update_data.keys()
        vals = ["'{}'".format(update_data[key]) if isinstance(update_data[key], str) else update_data[key] for key in
                keys]
        sql = 'insert into {}({}) VALUES ({})'.format('user', ', '.join(keys), ', '.join(vals))
        cursor.execute(sql)
        self.conn.commit()
        return cursor.lastrowid
