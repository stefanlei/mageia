from sqlalchemy import MetaData, text, create_engine as sql_create_engine
from contextlib import contextmanager


class Dict(dict):
    def __getattribute__(self, item):
        return object.__getattribute__(self, item)

    def __getattr__(self, item):
        if item not in self.keys():
            return None
        return self[item]

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, item):
        del self[item]


def create_engine(*args, **kwargs):
    return sql_create_engine(*args, **kwargs)


class DB(object):

    def __init__(self, e):
        self.engine = e
        self.connection = self.engine.connect()

    @contextmanager
    def session(self):
        work = self.connection.begin()
        tables = MetaData(bind=self.engine, reflect=True).tables
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


class Connection(object):

    def __init__(self, sa_con, tables):
        self.sa_on = sa_con
        self.tables = tables

    def query_one(self, sql, **kwargs):
        rs = self._query(text(sql), **kwargs)
        try:
            return next(rs)
        except StopIteration:
            return None

    def query(self, sql, **kwargs):
        rs = self._query(text(sql), **kwargs)
        return list(rs)

    def query_page(self, sql, page=1, limit=20, **kwargs):
        full_sql = sql + f" limit {int(limit)} offset {int(page) - 1}"
        rs = self._query(text(full_sql), **kwargs)
        return list(rs)

    def add(self, table, data):
        t = self._get_table(table)
        if not isinstance(data, dict):
            raise TypeError("Must be dict-like !")
        rs = self._execute(t.insert(), **data)
        new = dict()
        for k, v in zip(t.primary_key, rs.inserted_primary_key):
            new[k.name] = v
        new.update(data)
        return new

    def delete(self, table, data):
        t = self._get_table(table)
        if not isinstance(data, dict):
            raise TypeError("Must be dict-like !")
        t, primary_key = self._check_primary(t, data)
        s = t.delete().where(t.c[primary_key.name] == data[primary_key.name])
        self._execute(s)
        return data

    def merge(self, table, data):
        t = self._get_table(table)
        if not isinstance(data, dict):
            raise TypeError("Must be dict-like !")
        t, primary_key = self._check_primary(t, data)
        sql = t.update().where(t.c[primary_key.name] == data[primary_key.name]).values(data)
        self._execute(sql)
        return data

    def execute(self, sql, **kwargs):
        return self._execute(text(sql), **kwargs).rowcount

    def add_many(self, table, data_list):
        t = self._get_table(table)
        res = self._execute_many(t.insert(), data_list)
        return res.rowcount

    def merge_many(self, table, data_list):
        t = self._get_table(table)

        if not isinstance(data_list, (list, tuple)):
            raise TypeError("Must be list-like !")

        row = data_list[0]
        primary_key = []
        columns = []

        for k, v in row.items():
            if k not in t.c:
                continue
            if k in t.primary_key:
                cond = f"{k}=:{k}"
                primary_key.append(cond)
            else:
                set_sql = f"{k}=:{k}"
                columns.append(set_sql)

        where = ' and '.join(primary_key)
        value = ' set ' + ','.join(columns)

        s = f"update {t.name} {value} where {where}"
        res = self._execute_many(text(s), data_list)
        return res.rowcount

    def _get_table(self, table):
        if table not in self.tables:
            raise Exception(f"Not found table '{table}'!")
        return self.tables[table]

    @classmethod
    def _check_primary(cls, table, data):

        for primary_key in table.primary_key:
            if primary_key.name in data.keys():
                return table, primary_key
        else:
            raise Exception(f"Miss primary key !")

    def _execute(self, sql, **kwargs):
        rs = self.sa_on.execute(sql, **kwargs)
        return rs

    def _execute_many(self, sql, data):
        if not isinstance(data, (list, tuple)):
            data = [data]
        data = [dict(d) for d in data]
        return self.sa_on.execute(sql, data)

    def _query(self, sql, **kwargs):
        rs = self.sa_on.execute(sql, **kwargs)
        col = rs.keys()

        def to_dict(row):
            r = Dict()
            for k, v in zip(col, row):
                r[k] = v
            return r

        return (to_dict(row) for row in rs)
