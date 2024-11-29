import sqlite3
con = sqlite3.connect("users.db")
cur = con.cursor()
def init():
    cur.execute("CREATE TABLE if not exists users(name varchar(30), age int(100), contact char(10));")

def insert(values):
    name, age, contact = values
    cur.execute(f'INSERT INTO users VALUES("{name}", {age}, "{contact}");')

def view(name, age):
    cur.execute(f"SELECT * FROM users WHERE name = '{name}' and age = {age};")
    res = [i for i in cur]
    return res
cur.execute("SELECT * FROM users;")
