import sqlite3
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()
# cursor.execute('''
#     create table student(
#         id integer primary key autoincrement not null,
#         name text,
#         age integer
#     )
# ''')
# info = cursor.execute('''
# select * from  sqlite_master
# ''')
# 建表
# sql = ('''
# create table customer(
#     id integer primary key autoincrement not null,
#     account integer not null,
#     password char(10) not null,
#     name text
# )
# ''')
# 数据插入
sql = ('''
ALTER TABLE polls_user DROP COLUMN user_id;

''')
# 删除表
# sql = ('''
# drop table customer
# ''')
info = cursor.execute(sql)
conn.commit()
print(info.fetchall())
conn.close()
