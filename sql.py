import sqlite3


async def db_start():
    global db, cur
    db = sqlite3.connect('mat.db')
    cur = db.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS user_data(user_id TEXT, art TEXT, detail size TEXT""")
    db.commit()


async def create_profile(user_id):
    cur.execute("""INSERT INTO user_data VALUES(?,?,?)""", (user_id, '', ''))
    db.commit()



