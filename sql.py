import sqlite3

import username as username


async def db_start():
    global db, cur
    db = sqlite3.connect('materials.db')
    cur = db.cursor()
    if db:
        print('База данных запущена!')
    cur.execute(
        """CREATE TABLE IF NOT EXISTS user_data(user_id INT, brand TEXT, 
        article TEXT, title TEXT, length INT, width INT)""")
    db.commit()


async def add_profile(user_id):
    user = cur.execute("""SELECT 1 FROM user_data WHERE user_id == '{key}'""".format(key=user_id)).fetchone()
    if not user:
        cur.execute("""INSERT INTO user_data VALUES(?,?,?,?,?,?)""",
                    (user_id, '', '', '', '', ''))
        db.commit()


async def add_item(state, user_id):
    async with state.proxy() as data:
        cur.execute("""INSERT INTO user_data VALUES(?,?,?,?,?,?)""", (user_id, data['brand'], data['article'],
                                                                      data['title'], data['length'], data['width']))
        # cur.execute("UPDATE user_data SET brand = '{}', article = '{}', title = '{}', length = '{}', width = '{}' "
        #             "WHERE user_id == '{}'".format(data['brand'], data['article'], data['title'],
        #                                            data['length'], data['width'], user_id))
        db.commit()
