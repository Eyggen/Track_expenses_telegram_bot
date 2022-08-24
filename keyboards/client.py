from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

b1 = KeyboardButton('/help')
b2 = KeyboardButton('/Додати')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.row(b1,b2)