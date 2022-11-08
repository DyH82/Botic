from aiogram import types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from Keyboards import *
from main import dp
from sql import *

storage = MemoryStorage()

HELP_COMMAND = """
<b>/start</b> - <em>начало работы с ботом</em>
<b>/description</b> - <em>описание бота</em>
<b>/help</b> - <em>список команд</em>
"""

# Машина состояний
class ItemState(StatesGroup):
    item_brand = State()
    item = State()
    item_name = State()
    item_length = State()
    item_width = State()

    search = State()

# функция старта бота
async def on_startup(_):
    await db_start()
    print('Бот успешно запущен!')

# Обработчик команды старт
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer(
        f'Привет, <b>{message.from_user.first_name}</b>! Добро пожаловать в бот по поиску остатков\nДля помощи нажми > /Меню',
        reply_markup=get_start_kb(), parse_mode='HTML')

# обработчик команды отмена
@dp.message_handler(commands=['cancel'], state='*')
async def cancel_command(message: types.Message, state: FSMContext):
    if state is None:
        return

    await state.finish()
    await message.answer('Вы отменили действие!'
                         )
    await message.answer('Выберите действие!',
                         reply_markup=get_positions_ikb()) # вызываем


@dp.message_handler(commands=['Меню'])
async def pos_command(message: types.Message):
    await message.answer('Просмотр/добавление материала',
                         reply_markup=get_positions_ikb())


def get_edit_position():
    pass


# Показывает все позиции в базе.
async def show_all_positions(callback: types.CallbackQuery, positions: list) -> None:
    for position in positions:
        await callback.message.answer(f"производитель: {position[1]}\n"
                                      f"артикул: {position[2]}\n"
                                      f"Название: {position[3]}\n"
                                      f"Размер детали: {str(position[4])}*{str(position[5])}\n"
                                      f"Спроси у: @{position[6]}",
                                      reply_markup=get_edit_position(position[0])
                                      )
    await callback.message.answer('Выберите действие', reply_markup=get_positions_ikb())

# обработчик кнопки "Просмотр всех позиций"
@dp.callback_query_handler(text='get_all_positions')
async def cb_get_all_positions(callback: types.CallbackQuery):
    positions = await get_all_positions()

    if not positions:
        await callback.message.delete()
        await callback.message.answer('В базе пусто!')
        return await callback.answer()

    await callback.message.delete()
    await show_all_positions(callback, positions)
    await callback.answer()


# включаем состояние для поиска
@dp.callback_query_handler(text='get_position_')
async def cb_get_position(callback: types.CallbackQuery) -> None:
    await callback.message.answer('Введите артикул материала для поиска\nили нажмите -> /cancel',
                                  reply_markup=get_cancel_kb(),
                                  )
    await ItemState.search.set()
    await callback.message.delete()
    await callback.answer()

# выдача результата по базе данных
@dp.message_handler(state=ItemState.search)
async def srch_item(message: types.Message, state: FSMContext) -> None:
    position = await get_position(message.text)
    if position:
        for pos in position:
            s = ' '.join(str(pos))
            await message.reply('получите распишитесь! \n'
                                '\n'
                                f'{pos[0]}'
                                f' размером: {str(pos[1])}*{str(pos[2])}\n'
                                f'обратись к @{pos[3]}'
                                )
        await message.answer('Выберите действие!', reply_markup=get_positions_ikb())
        await state.finish()
        # print(pos)
    else:
        await message.reply("Нету такого материала",
                            reply_markup=get_positions_ikb())
        await state.finish()


# это будет допиливаться
@dp.callback_query_handler(positions_cb.filter(action='delete'))
async def cb_delete_position(callback: types.CallbackQuery, callback_data: dict):
    await delete_position(callback_data['id'])

    await callback.message.reply('Ваш материал удален!')
    await callback.answer()


@dp.message_handler(commands=['description'])
async def desc_command(message: types.Message):
    await message.answer('описание бота')
    await message.delete()

#################

# @dp.message_handler(commands=['help'])
# async def help_command(message: types.Message):
#     await message.reply(HELP_COMMAND,
#                         parse_mode='HTML')
#     await message.delete()

# обработчик кнопки "Добавить материал"
@dp.callback_query_handler(text='add_new_position')
async def cb_add_new_position(callback: types.CallbackQuery) -> None:
    await callback.message.answer('Введите производителя(Бренд)\nили нажмите -> /cancel',
                                  reply_markup=get_cancel_kb())
    await callback.message.delete()
    await ItemState.item_brand.set()

# вносит данные, бренд материала
@dp.message_handler(state=ItemState.item_brand)
async def load_item_brand(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['item_brand'] = message.text
    await state.update_data(item_brand=message.text.capitalize()) # приравниваем к одному виду
    await message.reply('Введите буквенно-цифровой артикул латинскими буквами\nили нажмите -> /cancel')
    await ItemState.next()

# название материала
@dp.message_handler(state=ItemState.item)
async def load_item(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['item'] = message.text
    await state.update_data(item=message.text.capitalize()) # приравниваем к одному виду
    await message.reply('Введите название материала\nили нажмите -> /cancel')
    await ItemState.next()


@dp.message_handler(state=ItemState.item_name)
async def load_item_name(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['item_name'] = message.text
    await state.update_data(item_name=message.text.capitalize())  # приравниваем к одному виду
    await message.reply('Введите длину детали в "мм"\nили нажмите -> /cancel')
    await ItemState.next()

# проверка на ввод чисел
@dp.message_handler(lambda message: not message.text.isdigit(), state=ItemState.item_length)
async def chk_lenght(message: types.Message, state: FSMContext):
    await message.reply('Введите цифры!')


@dp.message_handler(state=ItemState.item_length)
async def load_item_length(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['item_length'] = message.text
    await state.update_data(item_length=message.text)
    await message.reply('Введите ширину детали в "мм" \nили нажмите -> /cancel')
    await ItemState.next()


@dp.message_handler(lambda message: not message.text.isdigit(), state=ItemState.item_width)
async def chk_width(message: types.Message, state: FSMContext):
    await message.reply('Введите цифры!')


@dp.message_handler(state=ItemState.item_width)
async def load_item_width(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['item_width'] = message.text
    await state.update_data(item_width=message.text)
    await message.answer('Запись успешно добавлена в базу!',
                         reply_markup=get_start_kb())

    await add_item(state, username=message.from_user.username) # добавление всех значенний в базу данных

    await message.answer(f"производитель: {data['item_brand']}\n"
                         f"артикул: {data['item']}\n"
                         f"название: {data['item_name']}\n"
                         f"размер детали: {data['item_length'] + '*' + data['item_width']}")
    await state.finish()

####################### Удаление/редактирование элемента(admin)

@dp.callback_query_handler(positions_cb.filter(action='delete'))
async def cb_delete_position(callback: types.CallbackQuery, callback_data: dict):
    await sql.delete_position(callback_data['id'])

    await callback.message.reply('материал удален!')
    await callback.answer()

# @dp.callback_query_handler(positions_cb.filter(action='edit'))
# async def cb_edit_position(callback: types.CallbackQuery, callback_data: dict):
#     await callback.message.answer('Введи новый артикул')
#
#     await callback.message.reply('Материал отредактирован!')
#     await callback.answer()
