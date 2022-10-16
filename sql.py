import sqlite3


async def db_start():
    db = sqlite3.connect('materials.db')
    cur = db.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS user_data(item STRING, item_size STRING, user_id INT, username TEXT)""")
    db.commit()


async def add_det(user_id=None, username=None):
    # it = []
    # user_id = []
    # username = []
    item = input()
    item_size = input()
    db_u = sqlite3.connect('materials.db')
    cur = db_u.cursor()

    # it.append(it)
    cur.execute("""INSERT INTO user_data(item, item_size, user_id, username) VALUES(?,?,?,?)""",
                (item, item_size, user_id, username))
    db_u.commit()
    cur.close()

# def add_item(self, item_text):
#     stmt = "INSERT INTO items (description) VALUES (?)"
#     args = (item_text,)
#     self.conn.execute(stmt, args)
#     self.conn.commit()

# async def create_profile():
#     cur.execute("""INSERT INTO user_data VALUES(?,?,?)""", (user_id, user_name, ''))
#     db_u.commit()
