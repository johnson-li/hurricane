import pymysql

import hurricane.logging

logger = hurricane.logging.get_logger(__name__)


class Client(object):
    @staticmethod
    def wrap_val(val):
        if isinstance(val, (str, unicode)):
            return "'{}'".format(val)
        else:
            return val

    def get_connection(self):
        return pymysql.connect(user='root', db='hurricane')

    def get(self, table, db_filter=None, unique=False):
        connection = self.get_connection()
        with connection.cursor() as cursor:
            where_clause = 'where {}'.format(str(db_filter)) if db_filter else ''
            sql = 'select * from {} {}'.format(table, where_clause)
            logger.info(sql)
            cursor.execute(sql)
            res = cursor.fetchall()
            columns = [i[0] for i in cursor.description]
            res = [dict(zip(columns, user)) for user in res]
            return res[0] if unique else res

    def update(self, table, update_data={}, db_filter=None):
        connection = self.get_connection()
        with connection.cursor() as cursor:
            where_clause = 'where {}'.format(str(db_filter)) if db_filter else ''
            sql = 'update {} set {} {}'.format(table, ','.join(
                ['{} = {}'.format(key, Client.wrap_val(val)) for key, val in update_data.iteritems()]), where_clause)
            logger.info(sql)
            cursor.execute(sql)
        connection.commit()

    def create(self, table, update_data={}):
        connection = self.get_connection()
        with connection.cursor() as cursor:
            keys = update_data.keys()
            vals = [Client.wrap_val(update_data[key]) for key in keys]
            sql = 'insert into {}({}) VALUES ({})'.format(table, ', '.join(keys), ', '.join(vals))
            logger.info(sql)
            cursor.execute(sql)
        connection.commit()
        return cursor.lastrowid
