import sqlite3


async def db_start():
    global db, cur
    db = sqlite3.connect('materials.db')
    cur = db.cursor()
    if db:
        print('База данных запущена!')
    cur.execute(
        """CREATE TABLE IF NOT EXISTS user_data(user_id INT, brand TEXT, 
        article TEXT, title TEXT, length INT, width INT, username TEXT)""")

    db.commit()


# async def add_profile(user_id, username):
#     user = cur.execute("""SELECT 1 FROM user_data WHERE user_id == '{key}'""".format(key=user_id)).fetchone()
#     if not user:
#         cur.execute("""INSERT INTO user_data VALUES(?,?,?,?,?,?,?)""",
#                     (user_id, '', '', '', '', '', username))
#         db.commit()


async def add_item(state, user_id, username=None):
    async with state.proxy() as data:
        cur.execute("""INSERT INTO user_data VALUES(?,?,?,?,?,?,?)""", (user_id, data['brand'], data['article'], data['title'], data['length'], data['width'], username))
        # cur.execute("UPDATE user_data SET brand = '{}', article = '{}', title = '{}', length = '{}', width = '{}' WHERE user_id == '{}', username == '{}'".format(data['brand'], data['article'], data['title'], data['length'], data['width'],  user_id, username))
        db.commit()

# def add_item(self, item_text):
#     stmt = "INSERT INTO items (description) VALUES (?)"
#     args = (item_text,)
#     self.conn.execute(stmt, args)
#     self.conn.commit()

# async def create_profile():
#     cur.execute("""INSERT INTO user_data VALUES(?,?,?)""", (user_id, user_name, ''))
#     db_u.commit()
