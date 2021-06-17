from .connection import Connection, ConnectionSlave
from sqlalchemy import MetaData
from .db import create_engine
from contextlib import contextmanager
from .loadbalance import FullRandom


class ProxyDB(object):

    def __init__(self, settings, balance_class=None):
        self.balance = balance_class
        master_engine = create_engine(settings.get("master"))
        self.master_connection = master_engine.connect()
        self.slave_connection_mapper = dict()
        for slave in settings.get("slave"):
            slave_engine = create_engine(slave.get("url"))
            connection = slave_engine.connect()
            self.slave_connection_mapper[connection] = slave.get("optional")

    @contextmanager
    def session_slave(self):
        if self.balance is None:
            self.balance = FullRandom
        balance = self.balance()
        slave_connection = balance.get_slave(self.slave_connection_mapper)
        work = slave_connection.begin()
        meta = MetaData(bind=slave_connection)
        meta.reflect()
        tables = meta.tables
        try:
            connection = ConnectionSlave(slave_connection, tables)
            yield connection
            work.commit()
        except Exception as e:
            work.rollback()
            raise e

    @contextmanager
    def session(self):
        work = self.master_connection.begin()
        meta = MetaData(bind=self.master_connection, )
        meta.reflect()
        tables = meta.tables
        try:
            connection = Connection(self.master_connection, tables)
            yield connection
            work.commit()
        except Exception as e:
            work.rollback()
            raise e

    def query_one(self, sql, session=None, **kwargs):
        if session:
            return session.query_one(sql, **kwargs)
        with self.session_slave() as session:
            return session.query_one(sql, **kwargs)

    def query_page(self, sql, session=None, **kwargs):
        if session:
            return session.query_page(sql, **kwargs)
        with self.session_slave() as session:
            return session.query_page(sql, **kwargs)

    def query(self, sql, session=None, **kwargs):
        if session:
            return session.query(sql, **kwargs)
        with self.session_slave() as session:
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
