import os
from datetime import datetime
from pathlib import Path

from aiogram import Dispatcher, types
from aiogram.types import Message, ReplyKeyboardRemove

from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text

from create_bot import con, bot, logger,superuser,dp

from tgbot.keyboards.client_kb import knopki
from tgbot.keyboards.inline import gen_markup
from .kwit import readxls

def rootpath() -> Path:
    """Returns project root folder."""
    return str(Path(__file__).parent.parent.parent)  # Тут выход в корень проекта //TODO выход в корень проекта


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
    btn1 = types.KeyboardButton(text="Registratsiya", request_contact=True)
    key1 = types.ReplyKeyboardMarkup(resize_keyboard=True).add(btn1)

    await message.answer("Registratsiya qilish (pastdagi knopkani bosing)", reply_markup=key1)


# ловим первый ответ и пишем словарь
async def send_phone(message: types.Message, state=FSMContakt):
    async with state.proxy() as data:
        tel = str(message.contact.phone_number).strip()
        data['idp'] = int(str(message.contact.user_id).strip())
        data['phone'] = int(''.join(tel.split(' ')))
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
            innz = 0
        data['innorg'] = innz

    now = datetime.now()  # current date and time
    date_time = now.strftime("%Y.%m.%d %H:%M:%S") + ':'

    # Это до state.finish()
    if innz !=0:
        if await con.inn_exists(state):
            if not await con.user_exists(state):
                await con.add_user(state, date_time)
            else:
                await con.up_user(state, date_time)

            logger.info(f"\nRegistratsiya: {data['innorg']} {data['idp']} {data['phone']} {data['fio']}")
            await message.answer("/help")
        else:
            # Если в таблице ORG не будет INN
            # не будем регистрироват
            # print(date_time,data['innorg'],"Нет такой INN")
            logger.info(f"{data['innorg']} Нет такой INN")
            await message.answer(f"{data['innorg']} INN ro'yhatda mavjud emas, qaytadan /start")
        # Это до state.finish()
    else:
        await message.reply(f"INN raqami 9 xonali son bo'lishi kerak, qaytadan /start")
    await state.finish()

#    print(tuple(data.values()))  # Шу ерда хам ишлаяпти   state.finish() дан олдин булишши керак эди

# Выход из состояний
async def cancel_hendler(message: types.Message, state=FSMContakt):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('OK !')
    await message.answer("/help")

async def rek(message: types.Message):
    z = await con.get_inn(message.from_user.id)
    if z==None:
        s = '<b>Registratsiyadan qilinmagansiz.</b>   /start'
    else:
        s = f"<code>    id: {message.from_user.id}\n   Fio: {z[2]}\n   Tel: {z[1]}\nInnOrg: {z[0]}\nNamOrg: {z[4]}</code>"

    logger.info(f"\n{message.from_user.id} /rek rekvizitlarim {s}")
    await message.answer(s)


# @dp.message_handler(commands=["help"])
async def ok(message: types.Message):
    logger.info(f"\n{message.from_user.id} /ok")
    logger.info(f"Admin uchun id_user={message.from_user.id}")

    z = await con.get_inn(message.from_user.id)
    #print(f"{z=} {message.from_user.id=} ")
    if (z == None):
        s = f"<b>{message.from_user.full_name} registratsiya qilinmagan.</b>"
        await message.answer(s+'   /start')
    else:
        s = f"<code>    id: {message.from_user.id}\n   Fio: {z[2]}\n   Tel: {z[1]}\nInnOrg: {z[0]}\nNamOrg: {z[4]}</code>"
        await message.answer(s)

    if (message.chat.type == 'private'):
        logger.info(f"\n{message.from_user.id} /ok")
        await bot.send_message(superuser, f"User: {message.from_user.id}\n{s}")


async def help(message: types.Message):
    # TODO  /help
    admins_tab = await con.admins()
    hlp = "/start - Registratsiya\n/rek  - rekvizitlarim\n/ok - Status\n"
    if (message.from_user.id  in admins_tab):
        hlp = hlp + "\n/sendall INN Text - 'INN odamlariga Text yuborish'"
        hlp = hlp + "\n/dirx INN  - 'INN hisobotlarini ko'rish'\n/my  - mening tashkilotlarim\n"
    if message.from_user.id == superuser:  # superUser
        hlp = hlp + "\nSuperuser\n\n/reg  'INN, ID, TEl, FIO' регистрация User a\n/users - список Userов\n/addinn INN N namorg"
        hlp = hlp + "\n/delinn INN"
        hlp = hlp + "\n/inns - 'список ORG'\n/dir - 'список файлов'\n/del имя_файла -'Удаление файла'\n"
        hlp = hlp + "\n/addadmin - 'addadmin ID,INNORG,FIO'\n/deladmin - 'deladmin ID'\n/admins\n/sendadm - 'sendadm text'\n"
        hlp = hlp + "\n/copy\n/copybase\n/copylog\n/droplog - очистка Log файла"
    # await message.answer('<code>' + hlp + '</code>')
    logger.info(f"\n{message.from_user.id} /help")
    await message.answer(hlp)

    btn2 = types.KeyboardButton(text="/Oylik")
    key2 = types.ReplyKeyboardMarkup(resize_keyboard=True).add(btn2)
    await message.answer("<b>/Oylik tugmasini bosing</b>", reply_markup=key2)

async def kwitok(msg: Message):
    # TODO  kwitok
    inn = await con.get_inn(msg.from_user.id)
    logger.info(f"{msg.from_user.id} /Oylik")
    #print(knopki())
    markup = gen_markup(knopki(), "9999_99", 4)
    if inn==None:
        logger.info(f"\n{msg.from_user.id} not found in CLIENT... Qayta registratsiya qiling.")
        await msg.answer(f"Qayta registratsiya qiling.  /start")
    else:
        await msg.answer(f"<b>{inn[0]}: {inn[4]}.\n{msg.from_user.full_name}.\nKerakli oyni tanlang.</b>", reply_markup=markup)
@dp.callback_query_handler(lambda c: c.data and c.data[4]=='_')
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    code = callback_query.data

    if code !='9999_99':
        #await callback_query.message.answer('Biroz kutib turing!')
        idd = callback_query.from_user.id
        x = await con.get_inn(idd)
        inn = 0
        phoneNumber = ''
        if x != None:
            inn = x[0]
            phoneNumber = '+' + str(x[1])
        logger.info(f"{idd} khopka {code}")
        #logger.info(f"{idd} {phoneNumber} 'Bazadan' {x}")

        path_sep = os.path.sep
        fil = rootpath() + path_sep + 'files' + path_sep + str(inn) + '_' + code + '.xls'

        #logger.info(f"{fil}")

        rt = await readxls(code,fil, phoneNumber, inn)

        #print(rt)
        if (rt[0] > 0):
            for ms in rt[1]:
                await callback_query.message.answer('<pre>' + ms + '</pre>')
            await bot.send_message(superuser, f"User: {inn} {callback_query.from_user.id} {callback_query.from_user.full_name} {code} kwitokni oldi.")
            logger.info(f"{inn} {callback_query.from_user.id} {code} kwitokni oldi.")
        else:
            await callback_query.message.answer(rt[1][0])
            await bot.send_message(superuser, f"User: {callback_query.from_user.id} {callback_query.from_user.full_name} {rt[1][0]}")
            logger.info(f"\n{callback_query.from_user.id} {rt[1][0]}")
    try:
        #print(f"{code=}")
        await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
        logger.info(f"{callback_query.from_user.id}  InlineKeyboards deleted.")
    except:
        logger.info(f"Ощибка при удаление InlineKeyboards.")

async def echo_info(message: types.Message):
    logger.info(f"{message.from_user.id}  Noma'lum komanda berildi")
    await message.answer("Noma'lum komanda berildi. /help")


def register_user(dp: Dispatcher):
    dp.register_message_handler(com_start, commands=["start"])
    dp.register_message_handler(send_phone, content_types=['contact'], state=FSMContakt.phone)
    dp.register_message_handler(load_inn, state=FSMContakt.innorg)
    dp.register_message_handler(cancel_hendler, state="*", commands=["otmena"])
    dp.register_message_handler(cancel_hendler, Text(equals="otmena", ignore_case=True), state="*")
    dp.register_message_handler(ok, commands=["ok"])
    dp.register_message_handler(rek, commands=["rek"])
    dp.register_message_handler(help, commands=["help","?"])
    dp.register_message_handler(kwitok,commands=["Oylik"])
    dp.register_message_handler(echo_info)
