from sqlalchemy import text
from .common import Dict


class ConnectionBase(object):
    def __init__(self, sa_con, tables):
        self.sa_on = sa_con
        self.tables = tables

    def _get_table(self, table):
        if table not in self.tables:
            raise Exception(f"Not found table '{table}'!")
        return self.tables[table]

    @classmethod
    def _check_primary(cls, table, data):
        primary_key_list = []
        for primary_key in table.primary_key:
            if primary_key.name not in data.keys():
                raise Exception(f"The primary key is incomplete, miss {primary_key.name} !")
            primary_key_list.append(primary_key)
        return table, primary_key_list

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


class WriteMix(object):

    def add(self, table, data):
        t = self._get_table(table)
        if not isinstance(data, dict):
            raise TypeError("Must be dict-like !")
        rs = self._execute(t.insert(), **data)
        new = Dict()
        for k, v in zip(t.primary_key, rs.inserted_primary_key):
            new[k.name] = v
        new.update(data)
        return new

    def delete(self, table, data):
        data = Dict(data)
        t = self._get_table(table)
        if not isinstance(data, dict):
            raise TypeError("Must be dict-like !")
        t, primary_key_list = self._check_primary(t, data)

        primary_key = []

        for key, val in data.items():
            if key not in t.c:
                continue
            if key in t.primary_key:
                cond = f"{key}=:{key}"
                primary_key.append(cond)

        where = ' and '.join(primary_key)
        s = f"delete from {t.name} where {where}"

        res = self.sa_on.execute(text(s), data)
        return data

    def execute(self, sql, **kwargs):
        return self._execute(text(sql), **kwargs).rowcount

    def add_many(self, table, data_list):
        t = self._get_table(table)
        res = self._execute_many(t.insert(), data_list)
        return res.rowcount

    def merge(self, table, data):
        data = Dict(data)
        t = self._get_table(table)
        if not isinstance(data, dict):
            raise TypeError("Must be dict-like !")
        t, primary_key_list = self._check_primary(t, data)

        primary_key = []
        columns = []

        for key, val in data.items():
            if key not in t.c:
                continue
            if key in t.primary_key:
                cond = f"{key}=:{key}"
                primary_key.append(cond)
            else:
                set_sql = f"{key}=:{key}"
                columns.append(set_sql)

        where = ' and '.join(primary_key)
        value = ' set ' + ','.join(columns)

        s = f"update {t.name} {value} where {where}"

        res = self.sa_on.execute(text(s), data)
        return data

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
        pass

    def _execute_many(self, param, data_list):
        pass


class ReadMix(object):

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


class Connection(ConnectionBase, ReadMix, WriteMix):
    def __init__(self, sa_con, tables):
        super().__init__(sa_con, tables)

    def query_one(self, sql, **kwargs):
        return super().query_one(sql, **kwargs)

    def query(self, sql, **kwargs):
        return super().query(sql, **kwargs)

    def query_page(self, sql, page=1, limit=20, **kwargs):
        return super().query_page(sql, page, limit, **kwargs)

    def add(self, table, data):
        return super().add(table, data)

    def delete(self, table, data):
        return super().delete(table, data)

    def execute(self, sql, **kwargs):
        return super().execute(sql, **kwargs)

    def add_many(self, table, data_list):
        return super().add_many(table, data_list)

    def merge(self, table, data):
        return super().merge(table, data)

    def merge_many(self, table, data_list):
        return super().merge_many(table, data_list)


class ConnectionSlave(ConnectionBase, ReadMix):

    def query_one(self, sql, **kwargs):
        return super().query_one(sql, **kwargs)

    def query(self, sql, **kwargs):
        return super().query(sql, **kwargs)

    def query_page(self, sql, page=1, limit=20, **kwargs):
        return super().query_page(sql, page, limit, **kwargs)
