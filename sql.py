import sqlite3


# инициализируем создание базы данных, если она не создана
async def db_start():
    global db, cur
    db = sqlite3.connect('materials_1.db')
    cur = db.cursor()
    if db:
        print('База данных запущена!')
    cur.execute(
        """CREATE TABLE IF NOT EXISTS user_data(id INTEGER PRIMARY KEY, user_id INT, brand TEXT, 
        article TEXT, title TEXT, length INT, width INT, username TEXT, first_name TEXT)""")
    db.commit()


# выводим все значения из таблицы
async def get_all_positions():
    positions = cur.execute("SELECT * FROM user_data").fetchall()

    return positions


#  выводим некоторые значения, если результат пользователя совпадает с результатом БД
async def get_position(position=None):
    db = sqlite3.connect('materials_1.db')
    position = cur.execute(
        "SELECT user_id, article, length, width, username, first_name FROM user_data WHERE article LIKE ?",
        ('%' + str(position) + '%',)).fetchall()

    db.close()
    return position


# добавляем данные в таблицу
async def add_item(state, user_id=None, username=None, first_name=None):
    async with state.proxy() as data:
        position = cur.execute(
            "INSERT INTO user_data (user_id, brand, article, title, length, width, username, first_name) VALUES(?,?,?,?,?,?,?,?)",
            (user_id, data['item_brand'], data['item'], data['item_name'], data['item_length'], data['item_width'],
             username, first_name))

        db.commit()

    return position


# удаление/редактирование (админ)
async def delete_position(p_id: int) -> None:
    cur.execute("DELETE FROM user_data WHERE id =?", (p_id,))
    db.commit()

# async def edit_position(p_id: int) -> None:
#     cur.execute("DELETE FROM user_data WHERE id =?", (p_id,))
#     db.commit()
