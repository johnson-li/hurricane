import pymysql
import pymysql.err


def init_db():
    connection = pymysql.connect(user='root')
    with connection.cursor() as c:
        try:
            c.execute('drop database hurricane')
        except pymysql.err.InternalError:
            # if database hurricane does not exist, just skip
            pass
        c.execute('create database hurricane')
    connection = pymysql.connect(user='root', db='hurricane')
    with connection.cursor() as c:
        c.execute('CREATE TABLE User (user_id INTEGER PRIMARY KEY AUTO_INCREMENT, email TEXT, name TEXT, password TEXT, bio TEXT)')
        connection.commit()
    connection.close()


init_db()
