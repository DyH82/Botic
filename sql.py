import sqlite3


async def db_start():
    db = sqlite3.connect('materials.db')
    cur = db.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS user_data(detail_size TEXT, user_id INT, username TEXT)""")
    db.commit()


async def add_det(detail_size, user_id, username):
    # it = []
    # user_id = []
    # username = []
    db_u = sqlite3.connect('materials.db')
    cur = db_u.cursor()

    # it.append(it)
    cur.execute("""INSERT INTO user_data(detail_size, user_id, username) VALUES(?,?,?);""",
                (detail_size, user_id, username,))
    db_u.commit()
    cur.close()


# async def create_profile():
#     cur.execute("""INSERT INTO user_data VALUES(?,?,?)""", (user_id, user_name, ''))
#     db_u.commit()
