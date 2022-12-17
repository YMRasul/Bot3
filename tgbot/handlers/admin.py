from datetime import datetime
from aiogram import Dispatcher,types
from aiogram.types import Message
from create_bot import bot,con
from .user import rootpath
from tgbot.keyboards.client_kb import kb_client, mas
from tgbot.config import Config


#@dp.message_handler(commands=["start"], state="*", is_admin=True)
async def admin_start(message: Message):
    await message.answer("Скрепки ни босинг !\n Fayl   'NNNNNNNNN_gggg_mm.xls'  ko'rinishida bo'lishi kerak\n Misol 200918719_2022_11.xls")

async def user_reg(message: Message):
    user_id = message.from_user.id
    text = message.text[5:]
    try:
        print(text[0:9],text[10:],"-----> Регистрация по команде /reg 123456789 998937850078")
        inn = int(text[0:9])
        tel = int(text[10:])
        if await con.inn_exists2(inn):
            await  con.reg_id(user_id,inn,tel)
            await message.answer("Registrasiya qilindingiz ..."+str(user_id))
        else:
            await message.answer("Registrasiya ketmadi\nQaytadan registrasiya qiling !\n " + str(inn) +"ORG da mavjud emas")
    except:
        await message.answer("Registrasiya ketmadi\nQaytadan registrasiya qiling ! " + str(user_id))

async def user_info(message: Message):
    inn = await con.get_inn(message.chat.id)
    print(inn)
    await message.answer("Ma'lumot olish\n" + str(inn[0]), reply_markup=kb_client)

#@dp.message_handler(commands=["sendinn"], state="*", is_admin=True)
async def send_inn(message: Message):
    text=message.text[9:]
    mess = "/sendiin dan keyin probel\n" \
           "INN 9 hona raqam probel\n" \
           "va 1 hona raqam\n" \
           "123456789 1\n" \
           "********* * "
    if message.from_user.id == 139204666:    # superUser
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
async def send_all(message: Message):
    config: Config = bot.get('config')
    user_id = message.from_user.id
    print("Админстраторы " + str(config.tg_bot.admin_ids))
    r = await con.get_inn(user_id)
    if ((message.chat.type == 'private') and (r!=None)):
        text = message.text[9:]
        users = await con.get_users()
        if (users !=None):
            # idp,fio,prz,inn
            for row in users:
                try:
                    if row[1]==None:
                        row[1]=''
                    if row[3] == r[0]:
                        await bot.send_message(row[0], text)
                        if int(row[3]) != 1:
                           await con.set_active(1,row[0])
                        await bot.send_message(message.from_user.id, 'Рассылка' + ' ' + str(row[0]) + ": " + row[1])
                        print("Рассылка юзеру " + str(row[0]) + " " + row[1])
                except:
                    await con.set_active(0,row[0])
                    print("Юзер " + str(row[0]) + " " + row[1] + " не активен")

#@dp.message_handler(content_types=[types.ContentType.DOCUMENT])
async def scan_doc(message: types.document):
    try:
        file_info = await bot.get_file(message.document.file_id)
        downloaded_file = await bot.download_file(file_info.file_path)

        fil = rootpath() + '\\files\\'  # отвратительное решение
        src = fil + message.document.file_name

        now = datetime.now()  # current date and time
        date_time = now.strftime("%Y.%m.%d %H:%M:%S") + ':'

        foun = await con.poisk_id(message.from_user.id,message.document.file_name)
        if  foun:
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file.getvalue())
            print(date_time,"Сохранен как "+src)
            await message.answer("Men buni saqlab qoydim, rahmat!")
        else:
            await message.answer("Fayl qabul qilinmadi !")

    except Exception as e:
        await message.answer(e)

async def help(message: types.Message):
#    print("Help для Админа")
    hlp = "/start - Fayl jo'natish\n" \
          "/sendall - Hammaga habar yuborish\n" \
          "/sendinn - INN # \nQo'shish\nO'zgartirish\n" \
          "Olib tashlash #=9"
    hlp = hlp + "\n/reg 999999999 998991234567 - registratsiya\n999999999-INN 998991234567-tel\n/info - ma'lumot olish"
    await message.answer(hlp)

def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)
    dp.register_message_handler(user_reg, commands=["reg"],state="*", is_admin=True)
    dp.register_message_handler(user_info, commands=["info"],state="*", is_admin=True)
    dp.register_message_handler(send_inn, commands=["sendinn"], state="*", is_admin=True)
    dp.register_message_handler(send_all,commands=["sendall"],state="*" ,is_admin=True)
    dp.register_message_handler(scan_doc,content_types=[types.ContentType.DOCUMENT],is_admin=True)
    dp.register_message_handler(help,commands=["help"], state="*", is_admin=True)
