import unittest
import sys

sys.path.append("../mageia")
from mageia.db import DB, create_engine
from settings import url

engine = create_engine(url)
db = DB(engine)


class UserMultiplePK(unittest.TestCase):
    def test_delete(self):
        user = {"id": 3, "name": "delete_user", "age": 21}
        db.delete("user_multiple_pk", user)

        sql = "select * from user_multiple_pk where name=:name"
        db_user = db.query(sql, name="delete_user")
        self.assertEqual(db_user[0].id, 4)

    def test_merge(self):
        merge_user = {"id": 5, "name": "merge_user", "age": 30}
        db.merge("user_multiple_pk", merge_user)

        sql = "select * from user_multiple_pk where name=:name"
        db_user = db.query_one(sql, name="merge_user")
        self.assertEqual(db_user.age, 30)

    def test_merge_many(self):
        sql = "select * from user_multiple_pk"
        user_list = db.query(sql, name="merge_many_user")
        for user in user_list:
            user.age = 25
        db.merge_many("user_multiple_pk", user_list)
        db_user = db.query(sql, name="merge_many_user")
        for u in db_user:
            self.assertEqual(u.age, 25)

    def test_z_restore(self):
        db.execute("truncate table user_multiple_pk")
        db.add("user_multiple_pk", {"id": 1, "name": "stefan", "age": 19})
        db.add("user_multiple_pk", {"id": 2, "name": "tom", "age": 20})
        db.add("user_multiple_pk", {"id": 3, "name": "delete_user", "age": 21})
        db.add("user_multiple_pk", {"id": 4, "name": "delete_user", "age": 24})
        db.add("user_multiple_pk", {"id": 5, "name": "merge_user", "age": 24})
        db.add("user_multiple_pk", {"id": 6, "name": "merge_user", "age": 24})


if __name__ == '__main__':
    unittest.main()
