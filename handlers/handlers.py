from aiogram import types, F
from aiogram.filters.command import CommandStart, Command
from buttonkeyboard import get_genre_keyboard, get_regions_keyboard
from loader import dp, api_controller, bot, db_control
from aiogram.fsm.context import FSMContext


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    db_control.add_user(message.from_user.id)
    await message.answer(f"Доброго времени суток, {message.from_user.full_name}!\n"
                         f"Просмотр списка команд: /help")


@dp.message(Command('low'))
async def cmd_low(message: types.Message):
    db_control.add_history(message.from_user.id, 'low')
    await message.reply(api_controller.get_last_ten_chart_tracks(db_control.get_user_region(message.from_user.id)))


@dp.message(Command('high'))
async def cmd_low(message: types.Message):
    await message.reply(api_controller.get_first_ten_chart_tracks(db_control.get_user_region(message.from_user.id)))


@dp.message(Command('chart'))
async def cmd_low(message: types.Message):
    await message.reply(api_controller.get_all_chart(db_control.get_user_region(message.from_user.id)))


@dp.message(Command('custom'))
async def cnd_genre(message: types.Message, state: FSMContext):
    genre_dict = api_controller.get_genre_dictionary_from_chart(db_control.get_user_region(message.from_user.id))
    genre_keys = genre_dict.keys()
    await state.set_data({"genre": genre_dict})
    await message.reply('Какой жанр выберете:', reply_markup=get_genre_keyboard(genre_keys))


@dp.callback_query(F.data.startswith("genre:"))
async def callback_handler(callback: types.CallbackQuery, state: FSMContext):
    genre_name = callback.data.split(":")[1]
    genre_dict = (await state.get_data())['genre'][genre_name]
    genre_chart = api_controller.track_short_to_string(genre_dict, f'Треки в жанре {genre_name}:')
    await bot.send_message(callback.from_user.id, genre_chart)


@dp.message(Command('help'))
async def message_info(message: types.message):
    await message.reply(api_controller.commands_list())


@dp.message(Command('change'))
async def change_region(message: types.Message):
    set_region = db_control.get_user_region(message.from_user.id)
    all_regions = db_control.get_all_regions()
    await message.reply(f'Сейчас стоит регион {set_region}, на Какой хотите поменять: ',
                        reply_markup=get_regions_keyboard(all_regions))


@dp.callback_query(F.data.startswith("region:"))
async def callback_region(callback: types.CallbackQuery):
    region_name = callback.data.split(":")[1]
    db_control.change_region(callback.from_user.id, region_name)
    await bot.send_message(callback.from_user.id, f'Регион изменен на {region_name}')
    await callback.bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id, reply_markup=None)


@dp.message(Command('history'))
async def print_history(message: types.Message):
    await message.reply(db_control.get_user_history(message.from_user.id))


@dp.message(F.text)
async def error_text(message: types.Message):
    await bot.send_message(message.from_user.id, f'Такой команды нет, ознакомиться с ними можете по команде: /help')



