"Configure and initialize db"

import pymysql
from flask_sqlalchemy import SQLAlchemy
from flask import current_app
from flask import g

database = SQLAlchemy()
def connection():
    """ Connects database """
    if "db_conn" not in g:
        conf = current_app.config
        g.db_conn = pymysql.connect(
            host=conf["DB_HOST"],
            user=conf["DB_USER"],
            password=conf["DB_PASS"],
            db=conf["DB_NAME"],
            cursorclass=pymysql.cursors.DictCursor,
            charset="UTF8MB4"
        )

    return g.db_conn

def close():
    """ Closes database """
    conn = g.pop("db_conn", None)

    if conn is not None:
        conn.close()

def init_app(app):
    """ Initialize app """
    database.init_app(app)
    database.app = app
