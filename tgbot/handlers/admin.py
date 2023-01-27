from datetime import datetime
from aiogram import Dispatcher, types
from aiogram.types import Message
from create_bot import bot, con, superuser,logger  # ,today
from .user import rootpath
import os

async def adm_reg(message: Message):
    text = message.text[10:].strip()
    ms = [i.strip() for i in text.split(',')]

    if message.from_user.id == superuser:
        try:
            id = int(ms[0])
            innorg = int(ms[1])
            fio = ms[2]

            if await con.admin_add(id, innorg, fio) == None:
                await message.answer(str(id) + " registrasiya qilindi")
                #print(date_time,'Регистрация ', id, innorg, fio)
                logger.info(f"\n{message.from_user.id}: Registrasiya {id} {innorg} {fio}")
            else:
                await message.answer(str(id) + " rekvizitlari tuzatildi")
                #print(date_time,'Изменение реквизита', id, 'на', innorg, fio)
                logger.info(f"\n{message.from_user.id}: {id} rekvizitlri {innorg} {fio} ga almashdi")
        except:
            #print(date_time,'Registrasiya ketmadi ' + text + ' (/addadmin Number , Number , Text)')
            logger.info(f"\n{message.from_user.id}: Registrasiya ketmadi {text} (/addadmin Number , Number , Text)")
            await message.answer('Registrasiya ketmadi ' + text + ' (/addadmin Number , Number , Text)')
    else:
        #print(date_time,"Не SuperUser дает команду /addadmin")
        logger.info(f"\n{message.from_user.id}: Bu SuperUser ning komandasi  /addadmin")
        await message.answer("Это команда SuperUserа")


async def adm_del(message: Message):
    text = message.text[10:]
    s = text[0:].strip()
#    now = datetime.now()  # current date and time
#    date_time = now.strftime("%Y.%m.%d %H:%M:%S") + ':'
    if message.from_user.id == superuser:  # superUser
        try:
            id = int(s)
            #print(date_time,"Удаление по команде /deladmin", id)
            logger.info(f"\n{message.from_user.id}: Udaleniye po komande /deladmin {id}")
            if await con.admin_exists(id):
                await con.admin_del(id)
                await message.answer("Удален Admin id=" + str(id))
                #print(date_time,"Удален Admin id=" + str(id))
                logger.info(f"Admin {id} deleted")
            else:
                await message.answer(str(id) + " admin ro'yhatda mavjud emas")
                #print(date_time,str(id) + " такой админ в списке нет")
                logger.info(f"{id} not exist in table admin")
        except:
            await message.answer("Noto'g'ri id=" + s)
    else:
        #print(date_time,"Не SuperUser дает команду /deldmin")
        logger.info(f"/deladmin SuperUser komandasi")
        await message.answer("Это команда SuperUserа")

async def adm_info(message: Message):
    #text = '         id '+'   inn    '+'fio\n'
    text = ''
#    now = datetime.now()  # current date and time
#    date_time = now.strftime("%Y.%m.%d %H:%M:%S") + ':'
    if message.from_user.id == superuser:  # superUser
        r = await con.admins_info()
        if len(r) != 0:
            #print(date_time,"Результат команды /admins")
            logger.info(f"\n{message.from_user.id}: /admins komandasi natijasi")
            for m in r:
                #print(date_time,m[0], m[1], m[2],m[3])
                id = str(m[0]).rjust(12)
                org = m[3]
                fio = m[1]
                if (org is None):
                    org = 'not exist in ORG'
                logger.info(f"{id} {fio} {m[2]} {org}")
                text = text + id + ' ' + fio + '\n' + str(m[2]).rjust(12) + ' ' + org +"\n\n"
            await message.answer('<code>' + text+ '</code>')
        else:
            await message.answer("Admin lar ro'xati bo'sh ")
    else:
        #print(date_time,"Не SuperUser дает команду /admins")
        logger.info(f"\n{message.from_user.id}: /admins SuperUser komandasi")
        await message.answer("Это команда SuperUserа")

async def user_reg(message: Message):
    # TODO user_reg /reg INN,ID,TEl,FIO
    user_id = message.from_user.id
    text = message.text[5:].strip()
    ms = [i.strip() for i in text.split(',')]
    #print(ms)
    if message.from_user.id == superuser:  # superUser
        try:
            inn = int(ms[0])
            id  = int(ms[1])
            tel = int(ms[2])
            fio = ms[3]
            #print(f"{inn} {id} {tel} {fio}")
            logger.info(f"\nSuperUser /reg : {inn} {id} {tel} {fio}")
            if await con.inn_exists2(inn):
                await con.reg_id(id, inn, tel,fio)
                await message.answer(f"SuperUser registrasiya qildi.\n{ms}")
            else:
                await message.answer(
                f"Registrasiya ketmadi.\nINN {inn} ORG da mavjud emas.\nQaytadan registrasiya qiling.")
        except:
            await message.answer(f"Registrasiya ketmadi.\nQaytadanregistrasiya qiling.\n{ms}")
async def clients(message: Message):
    # TODO clients /list
    file1 = 'users.txt'
    if message.from_user.id == superuser:  # superUser
        r = await con.clients()
        i = 0
        with open(file1,'w', encoding="utf-8") as f:
            for z in r:
                i = i + 1
                f.write(f"{i}.  {z[0]} {z[1]} {z[2]} {z[3]} {z[4]}\n")
        logger.info(f"\n{message.from_user.id} Create List and Copy")
        src = rootpath() + os.path.sep + file1
        doc = open(src, 'rb')
        await message.reply_document(doc)
        logger.info(f"Created and getted file {src}")

# @dp.message_handler(commands=["sendinn"], state="*", is_admin=True)
async def send_inn(message: Message):
#    now = datetime.now()  # current date and time
#    date_time = now.strftime("%Y.%m.%d %H:%M:%S") + ':'
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
                #print(date_time,inn,prz,nam,"Delete INN " + str(inn))
                logger.info(f"\n{message.from_user.id}: {inn} {prz} {nam} Deleted INN {inn}")
            else:
                await message.answer("Insert or Update INN " + str(inn))
                #print(date_time,inn,prz,nam,"Insert or Update INN " + str(inn))
                logger.info(f"\n{message.from_user.id}: {inn} {prz} {nam} Inserted or Updated INN {inn}")
        except:
            await message.answer(mess)
    else:
        #print(date_time,"Не SuperUser дает команду /sendinn")
        logger.info(f"\n{message.from_user.id}: /sendinn this superusers command")
        await message.answer("Это команда SuperUserа")


# dp.register_message_handler(info_inn, commands=["inns"], state="*", is_admin=True)
async def info_inn(message: Message):
    # //TODO  info_inn
#    now = datetime.now()  # current date and time
#    date_time = now.strftime("%Y.%m.%d %H:%M:%S") + ':'
    if message.from_user.id == superuser:  # superUser
        logger.info(f"\n{message.from_user.id}/inns results")
        #print(f"\n{message.from_user.id}/inns results")
        inns = await con.inn_info()
        if inns:
            for inn in inns:
                r = await con.innUser(inn[0],1)
                act = str(r[0]).ljust(5)

                z = await con.innUser(inn[0],0)
                dea = str(z[0]).ljust(5)

                tot = str(r[0]+z[0]).ljust(5)

                s = f"{inn[0]} {inn[1]} {inn[2]}\nTotal: {tot}\nActiv: {act}\nNotac: {dea}"
                await message.answer('<code>' + s+ '</code>')
                #print(date_time,str(inn[1]) + ' ' + str(inn[0]) + ' ' + inn[2])
                logger.info(f"{inn[1]} {inn[0]} {inn[2]}")
        else:
            await message.answer('ORG is empty.')

    else:
        #print(date_time,"/inns SuperUser's command")
        logger.info(f"{message.from_user.id}\n/inns SuperUser's command")
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
        logger.info(f"Message {text}")
        if message.chat.type == 'private':
            logger.info(f"\n{message.from_user.id} /sendadm natijasi...")
            for adm in adms:
                s = str(adm[0]) + ' ' + adm[1] + ' ' + str(adm[2]) +' ' + adm[3]
                try:
                    await bot.send_message(adm[0], text)
                    await bot.send_message(message.from_user.id, s1 +s )
                    #print(date_time,"Рассылка админу " + s)
                    logger.info(f"Send to {s}")
                except:
                    await bot.send_message(message.from_user.id, "Admin " + s + " не активен")
                    #print(date_time,"Admin " + s + " не активен")
                    logger.info(f"Admin {s} not active")

# @dp.message_handler(commands=["sendall"], is_admin=True)
async def send_all(message: Message):
    '''
    Рассылка всем юзерам данного админа
    '''
    user_id = message.from_user.id
    #print("Админстраторы " + str(config.tg_bot.admin_ids))
    z = await con.get_rek(user_id)
    if ((message.chat.type == 'private') and (z != None)):
        logger.info(f"\n{message.from_user.id} /sendall natijasi...")
        logger.info(f"/sendall {z}")
        if z[2] == None:
            #print('У админа нет органиции с таким кодом',z[0])
            logger.info(f"Bu adminda {z[0]} kodli organitsiya yo'q")
            await message.answer('У админа нет органиции с таким кодом '+str(z[0]))
        else:
            text = message.text[9:]
            users = await con.get_users_org(z[0])
            if ((users != None) and (text!='') ):
                for row in users:
                    #now = datetime.now()  # current date and time
                    #date_time = now.strftime("%Y.%m.%d %H:%M:%S") + ':'
                    try:
                        if row[1] == None:
                            row[1] = ''
                        await bot.send_message(row[0], text)
                        if row[2] != 1:
                            await con.set_active(1, row[0])
                        await bot.send_message(message.from_user.id, str(row[0]) + ": " + row[1])
                        #print(date_time,"Рассылка юзеру",row[0],row[1],' от админа ',user_id,z[1],z[0],z[2])
                        logger.info(f"Admin {user_id} {z[1]} {z[0]} {z[2]} dan User {row[0]} {row[1]} uchun yuborildi")
                    except:
                        await con.set_active(0, row[0])
                        #print(date_time,"Юзер " + str(row[0]) + " " + row[1] + " не активен")
                        logger.info(f"User {row[0]} {row[1]} not active")
                await message.answer('Всем успешно отправлено.')
                logger.info(f"All sended ")


# @dp.message_handler(content_types=[types.ContentType.DOCUMENT])
async def scan_doc(message: types.document):
#    now = datetime.now()  # current date and time
#    date_time = now.strftime("%Y.%m.%d %H:%M:%S") + ':'
    try:
        file_info = await bot.get_file(message.document.file_id)
        downloaded_file = await bot.download_file(file_info.file_path)
        path_sep = os.path.sep
        fil = rootpath() + path_sep + 'files' + path_sep
        src = fil + message.document.file_name

        foun = await con.poisk_id(message.from_user.id, message.document.file_name)
        logger.info(f"\n{message.from_user.id} Screpki natijasi")
        if  foun:
            r = await con.get_innorg(message.from_user.id)
            #print(date_time,message.from_user.id,r[0],r[1],',',end=' ')
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file.getvalue())
            #print("сохранил как " + src)

            logger.info(f"{message.from_user.id} {r[0]} {r[1]} сохранил как {src}")
            await message.answer("Men buni saqlab qoydim, rahmat!")
        else:
            if message.from_user.id == superuser:  # superUser
                with open(src, 'wb') as new_file:
                    new_file.write(downloaded_file.getvalue())

                #print(date_time, superuser,'SuperUser',',' ,end=' ')
                #print("cохранил как " + src)
                logger.info(f"{superuser} SuperUser saved as {src}")
                await message.answer("SuperUser tomonidan saqlab qo'yildi.")
                #print(date_time,message.document.file_name, 'Не может быть сохранен, но SuperUser может сохранить.', message.from_user.id)
            else:
                logger.info(f"{message.document.file_name} fayli qabul qilinmadi.")
                await message.answer("Fayl qabul qilinmadi.")
    except Exception as e:
        await message.answer(e)

async def dirfiles(message: types.Message):
    if message.from_user.id == superuser:  # superUser
        logger.info(f"\n{message.from_user.id} /dir natijasi")
        path_sep = os.path.sep
        fil = rootpath() + path_sep + 'files' + path_sep
        f1 =''
        f2 =''
        for root, dirs, files in os.walk(fil):
            for filename in files:
                src = fil + filename
                f1 = f1  +  filename +'\n'
                f2 = f2 + src + '\n'
        await message.answer(f1)
        logger.info(f"\n{f2}")
async def deletefile(message: types.Message):
    if message.from_user.id == superuser:  # superUser
        filename = message.text[4:].strip()
        logger.info(f"\n{message.from_user.id} /del filename   natijasi")

        path_sep = os.path.sep
        fil = rootpath() + path_sep + 'files' + path_sep
        src = fil + filename
        if (os.path.isfile(src)):
            os.remove(src)
            logger.info(f"{src} deleted.")
            await message.answer(f"{filename} удален.")
        else:
            await message.answer(f"{filename} не найден.")
            logger.info(f"{src} not found.")
async def copydoc(message: types.Message):
    file1 = 'dbase_sqlite.db'
    if message.from_user.id == superuser:  # superUser
        logger.info(f"\n{message.from_user.id} /copy natijasi")
        path_sep = os.path.sep
        fil = rootpath() + path_sep + 'files' + path_sep
        fil1 = rootpath() + path_sep

        src = fil1 + file1
        doc = open(src, 'rb')
        i = 1
        await message.reply_document(doc)
#        print(date_time,i, 'Получен файл', src)
        logger.info(f"{i} getted file {src}")
        for root, dirs, files in os.walk(fil):
            for filename in files:
                src = fil + filename
                doc = open(src, 'rb')
                await message.reply_document(doc)
                i = i + 1
                logger.info(f"{i} getted file {src}")
                #print(date_time,i, 'Получен файл', src)

async def copylogfile(message: types.Message):
    file1 = 'oylikbot.log'
    if message.from_user.id == superuser:  # superUser
        logger.info(f"\n{message.from_user.id} /copylog natijasi")
        path_sep = os.path.sep
        fil1 = rootpath() + path_sep
        src = fil1 + file1
        doc = open(src, 'rb')
        await message.reply_document(doc)
        #        print(date_time,i, 'Получен файл', src)
        logger.info(f"getted file {src}")
async def droplogfile(message: types.Message):
    file1 = 'oylikbot.log'
    if message.from_user.id == superuser:  # superUser
        logger.info(f"\n{message.from_user.id} /droplog natijasi")
        path_sep = os.path.sep
        fil1 = rootpath() + path_sep
        src = fil1 + file1
        #doc = open(src, 'rb')
        with open(src, "w") as file:
            file.write("Start Log!!!\n")
        logger.info(f"Start Log {src}")
        await message.answer(f"dropped file {src}")

async def drop_org(message: types.Message):
    if message.from_user.id == superuser:  # superUser
        logger.info(f"\n{message.from_user.id} /droporg natijasi")
        #now = datetime.now()  # current date and time
        #date_time = now.strftime("%Y.%m.%d %H:%M:%S") + ':'
        await con.droporg()
        await message.answer('dropped table ORG ...')
        #print(date_time,'dropping table ORG ...')
        logger.info(f"dropped table ORG ...")


async def drop_adm(message: types.Message):
    if message.from_user.id == superuser:  # superUser
        logger.info(f"\n{message.from_user.id} /dropadm natijasi")
        #now = datetime.now()  # current date and time
        #date_time = now.strftime("%Y.%m.%d %H:%M:%S") + ':'
        await con.dropadm()
        await message.answer('dropped table ADMIN ...')
        #print(date_time,'dropped table ADMIN ...')
        logger.info(f"dropped table ADMIN ...")
def register_admin(dp: Dispatcher):
    dp.register_message_handler(adm_reg, commands=["addadmin"], state="*", is_admin=True)
    dp.register_message_handler(adm_del, commands=["deladmin"], state="*", is_admin=True)
    dp.register_message_handler(adm_info, commands=["admins"], state="*", is_admin=True)
    dp.register_message_handler(user_reg, commands=["reg"], state="*", is_admin=True)
    dp.register_message_handler(clients, commands=["list"], state="*", is_admin=True)
    dp.register_message_handler(send_inn, commands=["sendinn"], state="*", is_admin=True)
    dp.register_message_handler(info_inn, commands=["inns"], state="*", is_admin=True)
    dp.register_message_handler(send_adm, commands=["sendadm"], state="*", is_admin=True)
    dp.register_message_handler(send_all, commands=["sendall"], state="*", is_admin=True)
    dp.register_message_handler(scan_doc, content_types=[types.ContentType.DOCUMENT], is_admin=True)
    dp.register_message_handler(dirfiles, commands=["dir"], state="*", is_admin=True)
    dp.register_message_handler(deletefile, commands=["del"], state="*", is_admin=True)
    dp.register_message_handler(copydoc, commands=["copy"], state="*", is_admin=True)
    dp.register_message_handler(copylogfile, commands=["copylog"], state="*", is_admin=True)
    dp.register_message_handler(droplogfile, commands=["droplog"], state="*", is_admin=True)
    dp.register_message_handler(drop_org, commands=["droporg"], state="*", is_admin=True)
    dp.register_message_handler(drop_adm, commands=["dropadm"], state="*", is_admin=True)
