from functools import partial

import hurricane.db.impl.sqlite
import hurricane.logging
import hurricane.utils.exceptions

logger = hurricane.logging.get_logger(__name__)


class Client:
    def __init__(self):
        self.conn = hurricane.db.impl.sqlite.conn

    @staticmethod
    def wrap_val(val):
        if isinstance(val, str):
            return "'{}'".format(val)
        else:
            return val

    def get(self, table, db_filter=None, unique=False):
        cursor = self.conn.cursor()
        where_clause = 'where {}'.format(str(db_filter)) if db_filter else ''
        sql = 'select * from {} {}'.format(table, where_clause)
        logger.info(sql)
        cursor.execute(sql)
        res = cursor.fetchall()
        columns = [i[0] for i in cursor.description]
        res = [dict(zip(columns, user)) for user in res]
        return res[0] if unique else res

    def update(self, table, update_data={}, db_filter=None):
        cursor = self.conn.cursor()
        where_clause = 'where {}'.format(str(db_filter)) if db_filter else ''
        sql = 'update {} set {} {}'.format(table, ','.join(
            ['{} = {}'.format(key, Client.wrap_val(val)) for key, val in update_data.iteritems()]), where_clause)
        logger.info(sql)
        cursor.execute(sql)
        self.conn.commit()

    def create(self, table, update_data={}):
        cursor = self.conn.cursor()
        keys = update_data.keys()
        vals = [Client.wrap_val(update_data[key]) for key in keys]
        sql = 'insert into {}({}) VALUES ({})'.format(table, ', '.join(keys), ', '.join(vals))
        cursor.execute(sql)
        self.conn.commit()
        return cursor.lastrowid
