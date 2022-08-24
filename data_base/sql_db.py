import sqlite3 as sq
import re
from datetime import datetime
from create_bot import bot

r = re.compile('[^a-zA-Z]')

def sql_start():
    global r
    global base, cur
    try:
        base = sq.connect('Finance_bot.db')
        cur = base.cursor()
        if base:
            print("Succsed")
    except Exception as ex:
        print("nadazdelac")
        print(ex)

async def sql_add_table(user):
    try:
        base.execute('CREATE TABLE IF NOT EXISTS ' + user + '(obj, price, description, time, data)')
        base.commit()
    except Exception as ex:
        print("nadazdelac")
        print(ex) 

async def sql_add_row(user, obj, price, description):
    try:
        now = datetime.now()
        dt_string_data = now.strftime("%Y-%m-%d")
        dt_string_time = now.strftime("%H:%M:%S")
        cur.execute('INSERT INTO ' + user + ' VALUES (?,?,?,?,?)', (obj,price,description,dt_string_time,dt_string_data))
        base.commit()
    except Exception as ex:
        print("nadazdelac v db")
        print(ex)


async def return_data_from_db(message):
    user = 'U'+str(message.from_user.id)
    try:
        for row in cur.execute("SELECT * FROM " + user + " WHERE data == '" + message.text + "'").fetchall():
            #await bot.send_message(message.from_user.id, f'DATA= {row}, User= {str(message.text)}')
            await bot.send_message(message.from_user.id, f'Object: {row[0]}\nPrice: {row[1]}\nDecription: {row[2]}\nTime: {row[3]}, Data: {row[4]}')
    except:
        await bot.send_message(message.from_user.id, 'Шось пішло не так, перевірте правильність написання дати.')
    
async def print_sum(message, data):
    user = 'U'+str(message.from_user.id)
    month = {
    '12':'11-',
    '11':'10-',
    '10':'09-',
    '09':'08-',
    '08':'07-',
    '07':'06-',
    '06':'05-',
    '05':'04-',
    '04':'03-',
    '03':'02-',
    '02':'01-',
    '01':'12-'
    }
    if data[5:7] == '01':
        previous_data = str(int(data[0:4])-1) + '-'
    else:
        previous_data = data[0:4] + '-'

    previous_data = previous_data + month[data[5:7]]
    previous_data = previous_data + data[8:10]
    final_price = 0
    try:
        for price in cur.execute("SELECT price FROM " + user + " WHERE data == BETWEEN '" + previous_data +"' and '" + data +"'"):
            final_price += price
        await bot.send_message(message.from_user.id, f'Сума ваших витрат та прибутків = {final_price}')
    except Exception as ex:
        await bot.send_message(message.from_user.id, 'Шось пішло не так при обрахуванні суми витрат за місяць')

