import sqlite3


async def db_start():
    global db, cur
    db = sqlite3.connect('materials.db')
    cur = db.cursor()
    if db:
        print('База данных запущена!')
    # cur.execute(
    #     """CREATE TABLE IF NOT EXISTS user_data(user_id INT, brand TEXT,
    #     article TEXT, title TEXT, length INT, width INT, username TEXT)""")
    cur.execute(
        """CREATE TABLE IF NOT EXISTS user_data(id INTEGER PRIMARY KEY, brand TEXT, 
        article TEXT, title TEXT, length INT, width INT, username TEXT)""")

    db.commit()


async def get_all_positions():
    positions = cur.execute("SELECT * FROM user_data").fetchall()

    return positions


async def get_position():

    position = cur.execute("SELECT article FROM user_data WHERE article LIKE '%?%'").fetchall()

    return position


async def add_item(state, username=None):
    async with state.proxy() as data:
        # position = cur.execute(
        #     "INSERT INTO user_data (user_id, brand, article, title, length, width, username) VALUES(?,?,?,?,?,?,?)",
        #     (user_id, data['item_brand'], data['item'], data['item_name'], data['item_length'], data['item_width'],
        #      username))
        position = cur.execute(
                    "INSERT INTO user_data (brand, article, title, length, width, username) VALUES(?,?,?,?,?,?)",
                    (data['item_brand'], data['item'], data['item_name'], data['item_length'], data['item_width'],
                     username))

        db.commit()

    return position


async def delete_position(p_id: int) -> None:
    cur.execute("DELETE FROM user_data WHERE id =?", (p_id,))
    db.commit()
