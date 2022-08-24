from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from create_bot import dp, bot
from data_base import sql_db
from keyboards import kb_client
from datetime import datetime


class FSMClient(StatesGroup):
    obj = State()
    price = State()
    description = State()

class FSMReturn(StatesGroup):
    data_for_show = State()

# Старт
async def comands_start(message : types.Message):
    await sql_db.sql_add_table(user='U'+str(message.from_user.id))
    await bot.send_message(message.from_user.id, 'Початок роботи.', reply_markup=kb_client)

# Наводимо приклад опису речі
async def comands_help(message : types.Message):
    await message.answer("Введіть будь ласка ОДНУ річ або подію, на яку ви витралити кошти, а також кількість витрачених на неї кошт.\nБот опитавє вас, вам потрібно буде просто відповісти на його питання і він сам запише все що ви сказали.")
    await message.answer("Приклад: \nОбєкт: Крісло \nЦіна: -13000 \nОпис: Купив, геймерське крісло Dxracer master max. Мені зробили знижку через відсутність оригінальної подушки.")

# Початок зчитування подій
async def cm_start(message : types.Message):
    await FSMClient.obj.set()
    await message.reply('Що за річ/подія?')

# Зчитуємо назву
async def load_obj(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['obj'] = message.text
    await FSMClient.next()
    await message.reply('Тепер введи ціну(якщо витратив став - перед ціною, якщо ж заробив +)')

# Зчитуємо ціну
async def load_price(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = float(message.text)
    await FSMClient.next()
    await message.reply('Тепер можеш коротко описати цю річ/подію')

# Зчитуємо допис
async def load_description(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await FSMClient.next()
    name = 'U'+str(message.from_user.id)
    await message.answer('Обробляю данні')
    try:
        await message.answer(f"Name: {name}\nObject: {data['obj']}\nPrice: {data['price']}\nDecription: {data['description']}")
        await sql_db.sql_add_row(user=name,obj=data['obj'], price=data['price'], description=data['description'])
        await message.answer('Дані успішно надійшли на сервер.')
    except:
        await message.answer('Щось пішло не так при загрузі ваших даних на сервер.')
    await state.finish()


# Вихід зі стану 
async def cancel_hand(message : types.Message, state: FSMContext):
    cur_state = await state.get_state()
    if cur_state is None:
        return 
    await state.finish()
    await message.reply('OK')
    



async def cm_show(message: types.Message):
    await FSMReturn.data_for_show.set()
    await message.answer('Введіть дату для перегляду витрат та прибутуків за цю дату.')

async def ask_data(message: types.Message, state: FSMContext):
    await FSMReturn.next()
    await message.reply('Поняв')
    await sql_db.return_data_from_db(message)
    await state.finish()

async def show_sum(message: types.Message):
    await message.reply("OK")
    now_time = datetime.now()
    data = now_time.strftime("%Y-%m-%d")
    await sql_db.print_sum(message, data)

# Оголошуємо та привязуємо команди до функцій
def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(comands_help, commands=['help'])
    dp.register_message_handler(comands_start, commands=['start'])
    dp.register_message_handler(cm_start, commands='Додати', state=None)
    dp.register_message_handler(load_obj, state=FSMClient.obj)
    dp.register_message_handler(load_price, state=FSMClient.price)
    dp.register_message_handler(load_description, state=FSMClient.description)
    dp.register_message_handler(cancel_hand, state="*", commands='відміна')
    dp.register_message_handler(cancel_hand, Text(equals='відміна', ignore_case='True'), state='*')
    dp.register_message_handler(cm_show, commands='Вивести', state=None)
    dp.register_message_handler(ask_data, state=FSMReturn.data_for_show)
    dp.register_message_handler(show_sum, commands='Сума')