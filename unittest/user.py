import sys

sys.path.append("../mageia")

import unittest
from mageia.db import DB, create_engine, Dict
from datetime import datetime
from settings import url

engine = create_engine(url)
db = DB(engine)


class User(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)

    def test_1_query(self):
        sql = "select * from user where id = 1"
        user = db.query(sql)
        self.assertIsInstance(user, list)
        self.assertEqual(user[0].name, "Jack")

    def test_1_query_one(self):
        sql = "select * from user"
        user = db.query_one(sql)
        self.assertIsInstance(user, Dict)
        self.assertEqual(user.name, "Jack")

    def test_query_page(self):
        sql = "select * from user"
        user = db.query_page(sql, page=1, limit=2)
        self.assertEqual(2, len(user))
        self.assertEqual(user[0].name, "Jack")

    def test_insert(self):
        yak = Dict()
        yak.name = "Yak"
        yak.age = 29
        yak.addr = "nc"
        yak.birthday = datetime.now()
        db.add("user", yak)

        sql = "select * from user where name = :name"
        db_user = db.query_one(sql, name="Yak")
        self.assertEqual(db_user.name, "Yak")

    def test_z_restore(self):
        db.execute("truncate table user")
        db.add("user", {"id": 1, "name": "Jack", "age": 19, "addr": "sz", "birthday": datetime.now()})
        db.add("user", {"id": 2, "name": "Stefan", "age": 20, "addr": "nc", "birthday": datetime.now()})
        db.add("user", {"id": 3, "name": "Tom", "age": 21, "addr": "wh", "birthday": datetime.now()})
        db.add("user", {"id": 4, "name": "delete_user", "age": 21, "addr": "nc", "birthday": datetime.now()})
        db.add("user", {"id": 5, "name": "merge_user", "age": 21, "addr": "bj", "birthday": datetime.now()})
        db.add("user", {"id": 6, "name": "merge_many_user", "age": 21, "addr": "sh", "birthday": datetime.now()})
        db.add("user", {"id": 7, "name": "merge_many_user", "age": 21, "addr": "sh", "birthday": datetime.now()})
        self.test_1_query()

    def test_delete(self):
        user = {"id": 4, "name": "delete_user", "age": 21}
        db.delete("user", user)

        sql = "select * from user where name=:name"
        db_user = db.query_one(sql, name="delete_user")
        self.assertEqual(db_user, None)

    def test_merge(self):
        merge_user = {"id": 5, "name": "merge_user", "age": 33, "addr": "bj", "birthday": datetime.now()}
        db.merge("user", merge_user)

        sql = "select * from user where name=:name"
        db_user = db.query_one(sql, name="merge_user")
        self.assertEqual(db_user.age, 33)

    def test_merge_many(self):
        sql = "select * from user where name=:name"
        user_list = db.query(sql, name="merge_many_user")
        for user in user_list:
            user.age = 25
        db.merge_many("user", user_list)
        db_user = db.query(sql, name="merge_many_user")
        for u in db_user:
            self.assertEqual(u.age, 25)


if __name__ == '__main__':
    unittest.main()
