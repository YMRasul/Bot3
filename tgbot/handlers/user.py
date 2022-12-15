from datetime import datetime
from pathlib import Path

from aiogram import Dispatcher, types
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text

from create_bot import con

from tgbot.keyboards.client_kb import kb_client, mas
from .kwit import readxls


# async def user_start(message: Message):
#    await message.reply("Hello, user!")

def rootpath() -> Path:
    """Returns project root folder."""
    return str(Path(__file__).parent.parent.parent)  # Тут выход в корень проекта


'''
В качестве альтернативы указанию parent трижды можно:
Path(__file__).parents[2]
'''


class FSMContakt(StatesGroup):
    idp = State()
    phone = State()
    innorg = State()
    fio = State()


async def com_start(message: types.Message):
    await FSMContakt.phone.set()
    btn = types.KeyboardButton(text="Registratsiya", request_contact=True)
    key1 = types.ReplyKeyboardMarkup(resize_keyboard=True).add(btn)
    await message.answer("Registratsiya qilish (pastdagi knopkani bosing)", reply_markup=key1)


# ловим первый ответ и пишем словарь
async def send_phone(message: types.Message, state=FSMContakt):
    async with state.proxy() as data:
        data['idp'] = int(str(message.contact.user_id))
        data['phone'] = int(str(message.contact.phone_number))
        data['fio'] = message.contact.full_name
    await FSMContakt.next()
    await message.answer('Tashkilot INN raqamini yuboring !', reply_markup=ReplyKeyboardRemove())


# Ловим второй ответ
async def load_inn(message: types.Message, state=FSMContakt):
    innz = 0
    async with state.proxy() as data:
        if (len(message.text) == 9 and message.text.isdigit()):
            innz = int(message.text)
        else:
            await message.reply("/start INN raqami 9 xonali son bo'lishi kerak.")
            innz = 0

        data['innorg'] = innz

    now = datetime.now()  # current date and time
    date_time = now.strftime("%Y.%m.%d %H:%M:%S") + ':'

    # Это до state.finish()
    if await con.inn_exists(state):
        if not await con.user_exists(state):
            await con.add_user(state, date_time)
        else:
            await con.up_user(state, date_time)
        await message.answer("Ma'lumot olish uchun    /info")
    else:
        # Если в таблице ORG не будет INN
        # не будем регистрироват
        print(data['innorg'],"Нет такой INN")
        await message.answer("Bu INN ro'yhatda mavjud emas "+str(data['innorg']))
    # Это до state.finish()

    await state.finish()

#    print(tuple(data.values()))  # Шу ерда хам ишлаяпти   state.finish() дан олдин булишши керак эди

# Выход из состояний
async def cancel_hendler(message: types.Message, state=FSMContakt):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('OK !')
    await message.answer("Ma'lumot olish uchun    /info")


# ответ на команду /info
async def user_info(message: Message):
    inn = await con.get_inn(message.chat.id)
    print(inn)
    await message.answer("Ma'lumot olish\n" + str(inn[0]), reply_markup=kb_client)


# @dp.message_handler(content_types=[types.ContentType.DOCUMENT])
async def scan_doc(message: types.document):
    print("Mumkin emas, admin ro'yhatida mavjud emassiz.")
    await message.answer("Mumkin emas, admin ro'yhatida mavjud emassiz.")

#@dp.message_handler(commands=["sendinn"])
async def send_inn(message: Message):
    x = "Bu komanda superuser uchun qilingan !"
    print(x)
    await message.answer(x)

#@dp.message_handler(commands=["sendall"])
async def bot_send(message: Message):
    await message.answer("Это права Админа")


#@dp.message_handler(commands=["help"])
async def help(message: types.Message):
    print("Help для User")
    await message.answer("/start - Registratsiya\n/info - Ma'lumot olish")

async def echo_info(message: types.Message):
    idd = message.chat.id
    x = await con.get_inn(idd)
    inn = 0
    phoneNumber = ''
    if x != None:
        inn = x[0]
        phoneNumber = '+' + str(x[1])

    now = datetime.now()  # current date and time
    date_time = now.strftime("%Y.%m.%d %H:%M:%S") + ':'

    print(date_time, idd, phoneNumber, 'Bazadan', x)

    fil = rootpath() + '\\files\\' + str(inn) + '_' + message.text + '.xls'  # отвратительное решение

    if message.text == mas[0]:
        sss = await readxls(fil, phoneNumber)
        await message.answer(sss)
    elif message.text == mas[1]:
        sss = await readxls(fil, phoneNumber)
        await message.answer(sss)
    elif message.text == mas[2]:
        sss = await readxls(fil, phoneNumber)
        await message.answer(sss)
    elif message.text == mas[3]:
        sss = await readxls(fil, phoneNumber)
        await message.answer(sss)
    elif message.text == mas[4]:
        sss = await readxls(fil, phoneNumber)
        await message.answer(sss)
    elif message.text == mas[5]:
        sss = await readxls(fil, phoneNumber)
        await message.answer(sss)
    elif message.text == mas[6]:
        sss = await readxls(fil, phoneNumber)
        await message.answer(sss)
    elif message.text == mas[7]:
        sss = await readxls(fil, phoneNumber)
        await message.answer(sss)
    elif message.text == mas[8]:
        sss = await readxls(fil, phoneNumber)
        await message.answer(sss)
    elif message.text == mas[9]:
        sss = await readxls(fil, phoneNumber)
        await message.answer(sss)
    elif message.text == mas[10]:
        sss = await readxls(fil, phoneNumber)
        await message.answer(sss)
    elif message.text == mas[11]:
        sss = await readxls(fil, phoneNumber)
        await message.answer(sss)
    else:
        await message.answer("Noma'lum komada berildi.")


def register_user(dp: Dispatcher):
    dp.register_message_handler(com_start, commands=["start"], state="*")
    dp.register_message_handler(send_phone, content_types=['contact'], state=FSMContakt.phone)
    dp.register_message_handler(load_inn, state=FSMContakt.innorg)
    dp.register_message_handler(cancel_hendler, state="*", commands=["otmena"])
    dp.register_message_handler(cancel_hendler, Text(equals="otmena", ignore_case=True), state="*")
    dp.register_message_handler(user_info, commands=["info"])
    dp.register_message_handler(scan_doc, content_types=[types.ContentType.DOCUMENT])
    dp.register_message_handler(send_inn, commands = ["sendinn"])
    dp.register_message_handler(bot_send,commands=["sendall"])
    dp.register_message_handler(help, commands = ["help"])
    dp.register_message_handler(echo_info)
