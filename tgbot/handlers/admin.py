import shlex
from datetime import datetime
from aiogram import Dispatcher, types
from aiogram.types import Message
from create_bot import bot, con, superuser  # ,today
from .user import rootpath
from tgbot.keyboards.client_kb import kb_client  # , mas
from tgbot.keyboards.inline import inline_kb1
from tgbot.config import Config
import os, shutil

# @dp.message_handler(commands=["start"], state="*", is_admin=True)
'''
async def admin_start(message: Message):
    await message.answer(
        "Скрепки ни босинг !\n Fayl   'NNNNNNNNN_gggg_mm.xls'  ko'rinishida bo'lishi kerak\n Misol 200918719_2022_11.xls")
'''


async def adm_reg(message: Message):
    text = message.text[10:].strip()
    ms = [i.strip() for i in text.split(',')]
    now = datetime.now()  # current date and time
    date_time = now.strftime("%Y.%m.%d %H:%M:%S") + ':'

    if message.from_user.id == superuser:
        try:
            id = int(ms[0])
            innorg = int(ms[1])
            fio = ms[2]

            if await con.admin_add(id, innorg, fio) == None:
                await message.answer(str(id) + " registrasiya qilindi")
                print(date_time,'Регистрация ', id, innorg, fio)
            else:
                await message.answer(str(id) + " rekvizitlari tuzatildi")
                print(date_time,'Изменение реквизита', id, 'на', innorg, fio)
        except:
            print(date_time,'Registrasiya ketmadi ' + text + ' (/addadmin Number , Number , Text)')
            await message.answer('Registrasiya ketmadi ' + text + ' (/addadmin Number , Number , Text)')
    else:
        print(date_time,"Не SuperUser дает команду /addadmin")
        await message.answer("Это команда SuperUserа")


async def adm_del(message: Message):
    text = message.text[10:]
    s = text[0:].strip()
    now = datetime.now()  # current date and time
    date_time = now.strftime("%Y.%m.%d %H:%M:%S") + ':'
    if message.from_user.id == superuser:  # superUser
        try:
            id = int(s)
            print(date_time,"Удаление по команде /deladmin", id)
            if await con.admin_exists(id):
                await con.admin_del(id)
                await message.answer("Удален Admin id=" + str(id))
                print(date_time,"Удален Admin id=" + str(id))
            else:
                await message.answer(str(id) + " admin ro'yhatda mavjud emas")
                print(date_time,str(id) + " такой админ в списке нет")
        except:
            await message.answer("Noto'g'ri id=" + s)
    else:
        print(date_time,"Не SuperUser дает команду /regadmin")
        await message.answer("Это команда SuperUserа")


async def adm_info(message: Message):
    #text = '         id '+'   inn    '+'fio\n'
    text = ''
    now = datetime.now()  # current date and time
    date_time = now.strftime("%Y.%m.%d %H:%M:%S") + ':'
    if message.from_user.id == superuser:  # superUser
        r = await con.admins_info()
        if len(r) != 0:
            print(date_time,"Результат команды /admins")
            for m in r:
                print(date_time,m[0], m[1], m[2],m[3])
                text = text + str(m[2]) + ' ' + str(m[0]).rjust(12) +' '+  m[1] + ' ' + m[3]+ "\n"
            await message.answer('<code>' + text+ '</code>')
        else:
            await message.answer("Список админов пустой...")
    else:
        print(date_time,"Не SuperUser дает команду /admins")
        await message.answer("Это команда SuperUserа")

async def user_reg(message: Message):
    user_id = message.from_user.id
    text = message.text[5:]
    now = datetime.now()  # current date and time
    date_time = now.strftime("%Y.%m.%d %H:%M:%S") + ':'
    try:
        print(date_time,text[0:9], text[10:], "-----> Регистрация по команде /reg 123456789 998937850078")
        inn = int(text[0:9])
        tel = int(text[10:])
        if await con.inn_exists2(inn):
            await  con.reg_id(user_id, inn, tel)
            await message.answer("Registrasiya qilindingiz ..." + str(user_id))
        else:
            await message.answer(
                "Registrasiya ketmadi\nQaytadan registrasiya qiling !\n " + str(inn) + "ORG da mavjud emas")
    except:
        await message.answer("Registrasiya ketmadi\nQaytadan registrasiya qiling ! " + str(user_id))


async def user_info(message: Message):
    inn = await con.get_inn(message.chat.id)
    await message.answer("Ma'lumot olish\n" + str(inn[0]), reply_markup=kb_client)


# @dp.message_handler(commands=["sendinn"], state="*", is_admin=True)
async def send_inn(message: Message):
    now = datetime.now()  # current date and time
    date_time = now.strftime("%Y.%m.%d %H:%M:%S") + ':'
    text = message.text[9:]
    mess = " Xato,  /sendiin dan keyin probel\n" \
           "INN 9 hona raqam probel\n" \
           "keyin 1 hona raqam\n" \
           "va probel keyin nomi\n"
    if message.from_user.id == superuser:  # superUser
        try:
            inn = int(text[0:9])
            prz = int(text[10:11])
            nam = text[12:]
            # print(inn,'-',prz,'-',nam)
            await con.inn_add(inn, prz, nam)

            if prz == 9:
                await message.answer("Delete INN " + str(inn))
                print(date_time,inn,prz,nam,"Delete INN " + str(inn))
            else:
                await message.answer("Insert or Update INN " + str(inn))
                print(date_time,inn,prz,nam,"Insert or Update INN " + str(inn))
        except:
            await message.answer(mess)
    else:
        print(date_time,"Не SuperUser дает команду /sendinn")
        await message.answer("Это команда SuperUserа")


# dp.register_message_handler(info_inn, commands=["inns"], state="*", is_admin=True)
async def info_inn(message: Message):
    now = datetime.now()  # current date and time
    date_time = now.strftime("%Y.%m.%d %H:%M:%S") + ':'
    if message.from_user.id == superuser:  # superUser
        inns = await con.inn_info()
        if inns:
            for inn in inns:
                await message.answer(str(inn[1]) + ' ' + str(inn[0]) + ' ' + inn[2])
                print(date_time,str(inn[1]) + ' ' + str(inn[0]) + ' ' + inn[2])
        else:
            await message.answer('Список организаций пустой.')

    else:
        print(date_time,"Не SuperUser дает команду /inns")
        await message.answer("Это команда SuperUserа")


# @dp.message_handler(commands=["sendadm"], is_admin=True)
async def send_adm(message: Message):
    '''
    Рассылка всем админам  от SuperUser a
    '''
    now = datetime.now()  # current date and time
    date_time = now.strftime("%Y.%m.%d %H:%M:%S") + ':'
    text = message.text[9:]
    s1 = 'Админу '
    if ((message.from_user.id == superuser) and (text!='')):  # superUser
        adms = await con.admins_info()
        if message.chat.type == 'private':
            for adm in adms:
                s = str(adm[0]) + ' ' + adm[1] + ' ' + str(adm[2]) +' ' + adm[3]
                try:
                    await bot.send_message(adm[0], text)
                    await bot.send_message(message.from_user.id, s1 +s )
                    print(date_time,"Рассылка админу " + s)
                except:
                    await bot.send_message(message.from_user.id, "Admin " + s + " не активен")
                    print(date_time,"Admin " + s + " не активен")

# @dp.message_handler(commands=["sendall"], is_admin=True)
async def send_all(message: Message):
    '''
    Рассылка всем юзерам данного админа
    '''
    user_id = message.from_user.id
    #print("Админстраторы " + str(config.tg_bot.admin_ids))
    z = await con.get_rek(user_id)
    if ((message.chat.type == 'private') and (z != None)):
        now = datetime.now()  # current date and time
        date_time = now.strftime("%Y.%m.%d %H:%M:%S") + ':'
        print(date_time,'Админстратор',user_id,z)
        if z[2] == None:
            print('У админа нет органиции с таким кодом',z[0])
            await message.answer('У админа нет органиции с таким кодом '+str(z[0]))
        else:
            text = message.text[9:]
            users = await con.get_users_org(z[0])
            if ((users != None) and (text!='') ):
                for row in users:
                    now = datetime.now()  # current date and time
                    date_time = now.strftime("%Y.%m.%d %H:%M:%S") + ':'
                    try:
                        if row[1] == None:
                            row[1] = ''
                        await bot.send_message(row[0], text)
                        if row[2] != 1:
                            await con.set_active(1, row[0])
                        await bot.send_message(message.from_user.id, str(row[0]) + ": " + row[1])
                        print(date_time,"Рассылка юзеру",row[0],row[1],' от админа ',user_id,z[1],z[0],z[2])
                    except:
                        await con.set_active(0, row[0])
                        print(date_time,"Юзер " + str(row[0]) + " " + row[1] + " не активен")


# @dp.message_handler(content_types=[types.ContentType.DOCUMENT])
async def scan_doc(message: types.document):
    now = datetime.now()  # current date and time
    date_time = now.strftime("%Y.%m.%d %H:%M:%S") + ':'
    try:
        file_info = await bot.get_file(message.document.file_id)
        downloaded_file = await bot.download_file(file_info.file_path)
        path_sep = os.path.sep
        fil = rootpath() + path_sep + 'files' + path_sep
        src = fil + message.document.file_name

        foun = await con.poisk_id(message.from_user.id, message.document.file_name)
        if  foun:
            r = await con.get_innorg(message.from_user.id)
            print(date_time,message.from_user.id,r[0],r[1],',',end=' ')
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file.getvalue())
            print(date_time,"сохранил как " + src)
            await message.answer("Men buni saqlab qoydim, rahmat!")
        else:
            if message.from_user.id == superuser:  # superUser
                with open(src, 'wb') as new_file:
                    new_file.write(downloaded_file.getvalue())

                print(date_time, superuser,'SuperUser',',' ,end=' ')
                print("cохранил как " + src)
                await message.answer("SuperUser tomonidan saqlab qo'yildi.")
                print(date_time,message.document.file_name, 'Не может быть сохранен, но SuperUser может сохранить.', message.from_user.id)
            else:
                await message.answer("Fayl qabul qilinmadi !")
    except Exception as e:
        await message.answer(e)


async def copydoc(message: types.Message):
    now = datetime.now()  # current date and time
    date_time = now.strftime("%Y.%m.%d %H:%M:%S") + ':'
    file1 = 'dbase_sqlite.db'
    if message.from_user.id == superuser:  # superUser
        path_sep = os.path.sep
        fil = rootpath() + path_sep + 'files' + path_sep
        fil1 = rootpath() + path_sep

        src = fil1 + file1
        doc = open(src, 'rb')
        i = 1
        await message.reply_document(doc)
        print(date_time,i, 'Получен файл', src)

        for root, dirs, files in os.walk(fil):
            for filename in files:
                src = fil + filename
                doc = open(src, 'rb')
                await message.reply_document(doc)
                i = i + 1
                print(date_time,i, 'Получен файл', src)
async def drop_org(message: types.Message):
    if message.from_user.id == superuser:  # superUser
        now = datetime.now()  # current date and time
        date_time = now.strftime("%Y.%m.%d %H:%M:%S") + ':'
        await con.droporg()
        await message.answer('dropped table ORG ...')
        print(date_time,'dropping table ORG ...')


async def drop_adm(message: types.Message):
    if message.from_user.id == superuser:  # superUser
        now = datetime.now()  # current date and time
        date_time = now.strftime("%Y.%m.%d %H:%M:%S") + ':'
        await con.dropadm()
        await message.answer('dropped table ADMIN ...')
        print(date_time,'dropped table ADMIN ...')


async def help(message: types.Message):
    #    print("Help для Админа")
    hlp = "/start - Fayl jo'natish\n" \
          "/sendall - Hammaga habar yuborish\n"
    hlp = hlp + "/reg INN Tel -registratsiya\n     INN- 9 hona raqam, tel- 998 bilan\n\n/info - ma'lumot olish\n"

    if message.from_user.id == superuser:  # superUser
        hlp = hlp + "\nSuperuser\n\n/sendinn INN # namorg \n #\nДобавить\nИзменит\nУдалить #=9"
        hlp = hlp + "\n/inns - 'список ORG'\n"
        hlp = hlp + "\n/addadmin - 'addadmin ID,INNORG,FIO'\n/deladmin - 'deladmin ID'\n/admins\n/sendadm - 'sendadm text'"
        hlp = hlp + "\n/copy"
        hlp = hlp + "\n/droporg - сброс ORG\n/dropadm - сброс ADMIN"
    # await message.answer('<code>' + hlp + '</code>')
    await message.answer(hlp)


def register_admin(dp: Dispatcher):
    #    dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)
    dp.register_message_handler(adm_reg, commands=["addadmin"], state="*", is_admin=True)
    dp.register_message_handler(adm_del, commands=["deladmin"], state="*", is_admin=True)
    dp.register_message_handler(adm_info, commands=["admins"], state="*", is_admin=True)
    dp.register_message_handler(user_reg, commands=["reg"], state="*", is_admin=True)
    dp.register_message_handler(user_info, commands=["info"], state="*", is_admin=True)
    dp.register_message_handler(send_inn, commands=["sendinn"], state="*", is_admin=True)
    dp.register_message_handler(info_inn, commands=["inns"], state="*", is_admin=True)
    dp.register_message_handler(send_adm, commands=["sendadm"], state="*", is_admin=True)
    dp.register_message_handler(send_all, commands=["sendall"], state="*", is_admin=True)
    dp.register_message_handler(scan_doc, content_types=[types.ContentType.DOCUMENT], is_admin=True)
    dp.register_message_handler(copydoc, commands=["copy"], state="*", is_admin=True)
    dp.register_message_handler(drop_org, commands=["droporg"], state="*", is_admin=True)
    dp.register_message_handler(drop_adm, commands=["dropadm"], state="*", is_admin=True)
    dp.register_message_handler(help, commands=["help"], state="*", is_admin=True)
