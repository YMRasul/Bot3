from datetime import datetime
from aiogram import Dispatcher,types
from aiogram.types import Message
from create_bot import bot,con
from .user import rootpath

#@dp.message_handler(commands=["start"], state="*", is_admin=True)
async def admin_start(message: Message):
    await message.answer("Скрепки ни босинг !\n Fayl   'NNNNNNNNN_gggg_mm.xls'  ko'rinishida bo'lishi kerak\n Misol 200918719_2022_11.xls")

#@dp.message_handler(commands=["sendinn"], state="*", is_admin=True)
async def send_inn(message: Message):
    text=message.text[9:]
    mess = "/sendiin dan keyin probel\nINN 9 hona raqam probel\n va 1 hona raqam\n123456789 1\n********* * "
    if message.from_user.id == 1392046661:  # superUser
        if len(text) == 11:
            try:
                inn = int(text[0:9])
                prz = int(text[10:11])

                if prz==9:
                    await message.answer("Delete INN " + str(inn))
                else:
                    await message.answer("Insert or Update INN " + str(inn))

                await con.inn_add(inn,prz)
            except:
                await message.answer(mess)
        else:
            await message.answer(mess)
    else:
        print("Не SuperUser дает команду /sendinn" )
        await message.answer("Это команда SuperUserа")

#@dp.message_handler(commands=["sendall"], is_admin=True)
async def bot_send(message: Message):
    print("Отправка сообщении всем...",message.chat.id)
    await bot.send_message(chat_id=139204666, text='Shu habar bordimi ?')
    await message.answer("Всем")


#@dp.message_handler(content_types=[types.ContentType.DOCUMENT])
async def scan_doc(message: types.document):
    try:
        file_info = await bot.get_file(message.document.file_id)
        downloaded_file = await bot.download_file(file_info.file_path)

        fil = rootpath() + '\\files\\'  # отвратительное решение
        src = fil + message.document.file_name

        now = datetime.now()  # current date and time
        date_time = now.strftime("%Y.%m.%d %H:%M:%S") + ':'
        print(date_time,"Сохранен как "+src)

        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file.getvalue())

        await message.answer("Men buni saqlab qoydim, rahmat!")
    except Exception as e:
        await message.answer(e)

async def help(message: types.Message):
    print("Help для Админа")
    await message.answer("/start - Fayl jo'natish\n/sendall - Hammaga habar yuborish\n/sendinn - INN # \nQo'shish\nO'zgartirish\n#=9 Olib tashlash")

async def bot_echoall(message: types.document):
    print("Неправильная операция при отправке файла.")
    await message.answer("Noto'g'ri komanda berildi")


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)
    dp.register_message_handler(send_inn, commands=["sendinn"], state="*", is_admin=True)
    dp.register_message_handler(bot_send,commands=["sendall"],state="*" ,is_admin=True)
    dp.register_message_handler(scan_doc,content_types=[types.ContentType.DOCUMENT],is_admin=True)
    dp.register_message_handler(help,commands=["help"], state="*", is_admin=True)
    dp.register_message_handler(bot_echoall,state="*", content_types=types.ContentTypes.ANY,is_admin=True)
