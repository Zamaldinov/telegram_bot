from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, InlineKeyboardMarkup
from api import Controller


def get_genre_keyboard(key_list, kb_width: int = 3):
    buttons = []
    for i_genre in key_list:
        button = InlineKeyboardButton(text=str(i_genre), callback_data=f'genre:{i_genre}')
        buttons.append(button)
    genre_kb = InlineKeyboardBuilder().row(*buttons, width=kb_width).as_markup()
    return genre_kb


def get_regions_keyboard(region_list, kb_width: int = 3):
    buttons = []
    for i_region in region_list:
        button = InlineKeyboardButton(text=str(i_region[1]), callback_data=f'region:{i_region[1]}')
        buttons.append(button)
    genre_kb = InlineKeyboardBuilder().row(*buttons, width=kb_width).as_markup()
    return genre_kb
