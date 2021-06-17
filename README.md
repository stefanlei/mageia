# mageia





This is a simple database tools for MySQL

- Based on SQLAlchemy
- Transaction-Safe
- Friendly interface for developer
- Use `:param` syntax bind param
- Read/Write Splitting
- Load Balance

## Documentation

```
pip install mageia
```

##### Usage (DB)

```python
from mageia.db import DB, create_engine, Dict
url = "mysql+pymysql://root:password@localhost/info?charset=utf8"

# create a engine instance, and DB instance
engine = create_engine(url)
db = DB(engine)
```

##### Query

```python
# return [dict-like,dict-like,dict-like,] or None
user_list = db.query("select * from user where id=:id", id = 1)
user_list = db.query("select * from user where id in :id", id = [1,2,3])
user = user_list[0]
print(user.id)
print(user.name)
```

##### Query One

```python
# return dict-like or None
db.query_one("select * from user where id=:id", id = 1)
```

##### Query Page

```python
# return [dict-like,dict-like,dict-like,] or None
user = db.query_page("select * from user", page=1, limit=10)
```

##### Insert

```python
Jack = {
  "name":"Jack",
  "age":18,
  "sex":1
}
table = "user"

# Insert done, don't need commit
db.add(table, Jack)
```

##### Insert Many

```python
Jack = {
  "name":"Jack",
  "age":18,
  "sex":1
}
Tom = {
  "name":"Tom",
  "age":18,
  "sex":1
}
table = "user"
db.add_many(table, [Tom,Jack])
```

##### Delete

```python
data = db.query_one("select * from user where id = :id", id=1)
# Delete done, don't need commit, data must contain a primary key ,etc id .
db.delete("user", data)
```

##### Merge

```python
data = db.query_one("select * from user where id = :id", id=1)
# merge done, don't need commit, data must contain a primary key ,etc id .
data.name = "stefanlei"
db.merge("user",data)
```

##### Merge many

```python
user_list = db.query("select * from user where id in :ids", ids=[1, 2, 3, 4, 5, 6, 7, 8])

for user in user_list:
    user.name = "stefanlei"

db.merge_many("user", user_list)
```

##### Execute

```python
# return affected rows total
db.execute("delete from user where id = 1")
db.execute("update user set age = 18 where age = :age", age=16)
```

#### Transaction-Safe

You can also use `session` to keep `Transaction-Safe`

```python
# Use session to keep transaction-safe
with db.session() as s:
    db_user = s.query_one("select * from user")
    s.delete("user", db_user)

    user = Dict()
    user.name = "stefan"
    user.age = 18

    s.add("user", user)
```

---



##### Usage (ProxyDB)

```python
from mageia.proxy import ProxyDB

settings = {
    "master": "mysql+pymysql://user:password@192.168.1.1/mageia?charset=utf8",
    "slave": [
        {
            "url": "mysql+pymysql://user:password@192.168.1.2/mageia?charset=utf8",
            "optional": {
                "weight": 10
            }
        },
        {
            "url": "mysql+pymysql://user:password@192.168.1.3/mageia?charset=utf8",
            "optional": {
                "weight": 20
            }
        }
    ],
}

db = ProxyDB(settings)
```

##### Write (master)

```python
# Use session to keep transaction-safe ,and execute in master
with db.session() as s:
    sql = "select * from student"
    user = s.query_one(sql)

    user.age = 18
    s.merge("student", user)

    jack = {
        "name": "Jack",
        "age": 23
    }
    s.add("student", jack)
    
    s.delete("student", user)
```

##### read (slave)

```python
# Use session to keep transaction-safe ,and execute in slave
with db.session_slave() as s:
    sql = "select * from student"
    user = s.query_one(sql)
    
    user_list = s.query(sql)

    user_page = s.query_page(sql, page=1, limit=10)
```

##### Auto

```python
db = ProxyDB(settings)

# auto select master or slave

sql = "select * from student"
user = db.query_one(sql)

Jack = {
    "name": "Jack",
    "age": 18
}
db.add("student", Jack)

db.delete("student", user)
```

##### Load Balance

```python
from mageia.proxy import ProxyDB
from mageia.loadbalance import WeightRandom

settings = {
    "master": "mysql+pymysql://user:password@192.168.1.1/mageia?charset=utf8",
    "slave": [
        {
            "url": "mysql+pymysql://user:password@192.168.1.2/mageia?charset=utf8",
            "optional": {
                "weight": 10
            }
        },
        {
            "url": "mysql+pymysql://user:password@192.168.1.3/mageia?charset=utf8",
            "optional": {
                "weight": 20
            }
        }
    ],
}

# Load Balance Policy
db = ProxyDB(settings, balance_class=WeightRandom)
```

