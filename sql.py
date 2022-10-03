import sqlite3


async def db_start():
    global db_u, cur
    db_u = sqlite3.connect('mat.db')
    cur = db_u.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS user_data(user_id INT, username TEXT, detail_size TEXT)""")
    db_u.commit()


async def db_start():
    con = sqlite3.connect('mat.db')
    cursor = con.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS user_data(detail_size TEXT)""")
    con.commit()


async def add_det(item, user_id=None, user_name=None):
    global db_u, cur
    db_u = sqlite3.connect('mat.db')
    cur = db_u.cursor()
    a = []
    a.append(item)
    cur.execute("INSERT INTO user_data(user_id, username, detail_size) VALUES(?,?,?)",
                (user_id, user_name, a))
    db_u.commit()
    cur.close()


# async def create_profile():
#     cur.execute("""INSERT INTO user_data VALUES(?,?,?)""", (user_id, user_name, ''))
#     db_u.commit()
