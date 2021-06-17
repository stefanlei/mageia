from sqlalchemy import MetaData, create_engine as sql_create_engine
from contextlib import contextmanager
from .connection import Connection
from .common import Dict


def create_engine(*args, **kwargs):
    return sql_create_engine(*args, **kwargs)


class DB(object):

    def __init__(self, e):
        self.connection = e.connect()

    @contextmanager
    def session(self):
        work = self.connection.begin()
        meta = MetaData(bind=self.connection, )
        meta.reflect()
        tables = meta.tables
        try:
            connection = Connection(self.connection, tables)
            yield connection
            work.commit()
        except Exception as e:
            work.rollback()
            raise e

    def query_one(self, sql, session=None, **kwargs):
        if session:
            return session.query_one(sql, **kwargs)
        with self.session() as session:
            return session.query_one(sql, **kwargs)

    def query_page(self, sql, session=None, **kwargs):
        if session:
            return session.query_page(sql, **kwargs)
        with self.session() as session:
            return session.query_page(sql, **kwargs)

    def query(self, sql, session=None, **kwargs):
        if session:
            return session.query(sql, **kwargs)
        with self.session() as session:
            return session.query(sql, **kwargs)

    def add(self, table, d, session=None):
        if session:
            return session.add(table, d)
        with self.session() as session:
            return session.add(table, d)

    def merge(self, table, d, session=None):
        if session:
            return session.merge(table, d)
        with self.session() as session:
            return session.merge(table, d)

    def delete(self, table, d, session=None):
        if session:
            return session.delete(table, d)
        with self.session() as session:
            return session.delete(table, d)

    def execute(self, sql, session=None, **kwargs):
        if session:
            return session.execute(sql, **kwargs)
        with self.session() as session:
            return session.execute(sql, **kwargs)

    def add_many(self, table, data_list, session=None):
        if session:
            return session.add_many(table, data_list)
        with self.session() as session:
            return session.add_many(table, data_list)

    def merge_many(self, table, data_list, session=None):
        if session:
            return session.merge_many(table, data_list)
        with self.session() as session:
            return session.merge_many(table, data_list)
