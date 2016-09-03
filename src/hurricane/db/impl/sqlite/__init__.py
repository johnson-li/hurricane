import inspect
import logging
import os
import sqlite3

logger = logging.getLogger(__name__)

current_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
_db_file = '{}/sqlite.db'.format(current_dir)
os.remove(_db_file)
conn = sqlite3.connect(_db_file)


def init_db():
    c = conn.cursor()
    c.execute('CREATE TABLE User (user_id INTEGER PRIMARY KEY , email TEXT, name TEXT, password TEXT, bio TEXT)')
    conn.commit()


init_db()
