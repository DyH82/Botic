import sqlite3


async def db_start():
    db = sqlite3.connect('materials.db')
    cur = db.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS 'user_data'('user_id' INT, 'username' TEXT, 'detail_size' TEXT)""")
    db.commit()


async def add_det(it, user_id, username):

    db_u = sqlite3.connect('materials.db')
    cur = db_u.cursor()
    a = []
    a.append(it)
    cur.execute("""INSERT INTO user_data(detail_size, user_id, username) VALUES(?,?,?)""",
                (user_id, username, a))
    db_u.commit()
    cur.close()


# async def create_profile():
#     cur.execute("""INSERT INTO user_data VALUES(?,?,?)""", (user_id, user_name, ''))
#     db_u.commit()
