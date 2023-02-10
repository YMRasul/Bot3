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
                await message.answer(f"{id} {innorg} registrasiya qilindi")
                #print(date_time,'Регистрация ', id, innorg, fio)
                logger.info(f"\n{message.from_user.id}: Registrasiya {id} {innorg} {fio}")
            else:
                await message.answer(f"{id} {innorg} rekvizitlari tuzatildi")
                logger.info(f"\n{message.from_user.id}: {id} {innorg}  rekvizitlri {fio} ga almashdi")

        except:
            logger.info(f"\n{message.from_user.id}: Registrasiya ketmadi {text} (/addadmin Number , Number , Text)")
            await message.answer(f'Registrasiya ketmadi {text} (/addadmin Number , Number , Text)')
    else:
        #print(date_time,"Не SuperUser дает команду /addadmin")
        logger.info(f"\n{message.from_user.id}: Bu SuperUser ning komandasi  /addadmin")
        await message.answer("Это команда SuperUserа")

async def adm_del(message: Message):
    text = message.text[10:].strip()
    ms = [i.strip() for i in text.split(',')]
    if message.from_user.id == superuser:  # superUser
        try:
            id = int(ms[0])
            inn = int(ms[1])
            logger.info(f"{message.from_user.id}: Udaleniye po komande /deladmin {id},{inn}")
            if await con.admin_exists(id):
                if await con.inn_exists2(inn):
                    await con.admin_del(id, inn)
                    await message.answer(f"Удален Admin {id=} , {inn=}")
                    logger.info(f"Admin {id=} , {inn=} deleted")
                else:
                    await message.answer(f"Not deleted. {inn} INN ro'yhatda mavjud emas")
                    logger.info(f"Not deleted. {inn} INN ro'yhatda mavjud emas")
            else:
                await message.answer(f"Not deleted. {id} admin ro'yhatda mavjud emas")
                logger.info(f"Not deleted. {id} admin ro'yhatda mavjud emas")

        except:
            logger.info(f"{message.from_user.id}: Deladmin ketmadi {text} (/deladmin Number , Number)")
            await message.answer(f'Deladmin ketmadi {text} (/deladmin Number , Number)')

async def adm_info(message: Message):
    #text = '         id '+'   inn    '+'fio\n'
    text = ''
    if message.from_user.id == superuser:  # superUser
        r = await con.admins_info()
        if len(r) != 0:
            #print(date_time,"Результат команды /admins")
            logger.info(f"\n{message.from_user.id}: /admins komandasi natijasi")
            for m in r:
                #print(date_time,m[0], m[1], m[2],m[3])

                #print(m)

                id = str(m[0]).rjust(14)
                org = m[3].ljust(20)
                fio = m[1]
                if (org is None):
                    org = 'not exist in ORG'
                logger.info(f"{id} {m[2]} {org} [{fio}]")
                text = text + f"{id} {m[2]} {org} [{fio}]\n"

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
    text = message.text[8:]
    mess = " Xato,  /addiin dan keyin probel\n" \
       "INN 9 hona raqam probel\n" \
       "keyin 1 hona raqam\n" \
       "va probel keyin nomi\n"
    if message.from_user.id == superuser:  # superUser
        try:
            inn = int(text[0:9])
            prz = int(text[10:11])
            nam = text[12:]
            print(f"{inn=} {prz=} {nam=}")
            await con.inn_add(inn, prz, nam)
            await message.answer("Insert or Update INN " + str(inn))
            logger.info(f"{message.from_user.id}: {inn} {prz} {nam} Inserted or Updated INN {inn}")
        except:
            await message.answer(mess)
    else:
        #print(date_time,"Не SuperUser дает команду /sendinn")
        logger.info(f"{message.from_user.id}: /sendinn this superusers command")
        await message.answer("Это команда SuperUserа")
###################################################################
async def del_inn(message: Message):
    text = message.text[8:]
    mess = " Xato,  /deliin dan keyin probel\n" \
           "keyin INN 9 hona raqam\n"
    if message.from_user.id == superuser:  # superUser
        try:
            inn = int(text[0:9])
            #print(f"{inn=}")
            await con.inn_del(inn)
            await message.answer(f"Delete INN {inn}")
            #print(date_time,inn,prz,nam,"Delete INN " + str(inn))
            logger.info(f"{message.from_user.id}: Deleted INN {inn}")
        except:
            await message.answer(mess)
    else:
        #print(date_time,"Не SuperUser дает команду /sendinn")
        logger.info(f"\n{message.from_user.id}: /sendinn this superusers command")
        await message.answer("Это команда SuperUserа")


# dp.register_message_handler(info_inn, commands=["inns"], state="*", is_admin=True)
async def info_inn(message: Message):
    # //TODO  info_inn
    if message.from_user.id == superuser:  # superUser
        logger.info(f"{message.from_user.id}/inns results")
        #print(f"\n{message.from_user.id}/inns results")
        inns = await con.inn_info()
        s1=s2=s3=0
        s = 'ORG is empty.'
        if inns:
            s ='\n'
            for inn in inns:
                r = await con.innUser(inn[0],1)
                z = await con.innUser(inn[0],0)

                s1 = s1 + r[0]+z[0]
                s2 = s2 + r[0]
                s3 = s3 + z[0]

                s = s + f"{inn[0]} {inn[1]} {inn[2]}. ( {r[0]+z[0]},{r[0]},{z[0]} )\n"

            s = s + f"Users total {s1},{s2},{s3}\n"
            await message.answer('<b>' + s+ '</b>')
            #print(date_time,str(inn[1]) + ' ' + str(inn[0]) + ' ' + inn[2])
            logger.info(f"{s}")
        else:
            await message.answer(s)
            logger.info(f"{s}")

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

async def org(ms):
    kn =[]
    ln = len(ms)
    if ln > 0:
        for i in range(ln):
            kn.append(str(ms[i][0]).strip())
    return(kn)
async def send_all(message: Message):
    '''
    Рассылка всем юзерам организации данного админа
    '''
    msg = message.text[9:]
    inn = msg[0:9]
    txt = msg[10:]

    user_id = message.from_user.id
    #print("Админстраторы " + str(config.tg_bot.admin_ids))
    z = await con.get_rek(user_id)
    knp = await org(z)
    if inn in knp:
        #print(f"{inn} in {knp}")
        if (message.chat.type == 'private'):
            users = await con.get_users_org(int(inn))
            #print(f"{users=}")
            if (len(users) > 0):
                for row in users:
                    try:
                        if row[1] == None:
                            row[1] = ''

                        await bot.send_message(row[0], txt)

                        if row[2] != 1:
                            await con.set_active(1, row[0])

                        await bot.send_message(message.from_user.id, str(row[0]) + ": " + row[1])

                        logger.info(f"Admin {user_id} dan User {row[0]} {row[1]} uchun yuborildi")
                    except:
                        await con.set_active(0, row[0])
                        await bot.send_message(message.from_user.id,f"{row[0]} {row[1]} aktiv emas.")
                        logger.info(f"User {row[0]} {row[1]} not active")
            else:
                await bot.send_message(user_id, f"{inn} ishchilari registratsiydan o'tmagan")
    else:
        print('У админа нет органиции с таким кодом',inn)
        await message.answer(f"{message.from_user.full_name} {inn} ning adminstratori emas.")
# @dp.message_handler(content_types=[types.ContentType.DOCUMENT])
async def scan_doc(message: types.document):
    file_info = await bot.get_file(message.document.file_id)
    downloaded_file = await bot.download_file(file_info.file_path)
    path_sep = os.path.sep
    fil = rootpath() + path_sep + 'files' + path_sep
    src = fil + message.document.file_name

    if message.from_user.id == superuser:  # superUser
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file.getvalue())
        logger.info(f"{superuser} SuperUser saved as {src}")
        await message.answer("SuperUser tomonidan saqlab qo'yildi.")
    else:
        innfile = message.document.file_name[0:9]
        try:
            inn = int(innfile)
            adm = await con.poisk_id(message.from_user.id)
            #print(f"{inn=} {adm=}")
            logger.info(f"{message.from_user.id} Screpki natijasi")

            if (inn in adm):
                r = await con.get_innfio(message.from_user.id, inn)
                with open(src, 'wb') as new_file:
                    new_file.write(downloaded_file.getvalue())
                logger.info(f"{message.from_user.id} {inn} {r[0]} сохранил как {src}")
                await message.answer("Men buni saqlab qoydim, rahmat!")
                await bot.send_message(superuser, f"{message.document.file_name} User:{message.from_user.id} {inn} {r[0]} tomonidan yuborildi")
            else:
                logger.info(f"User={message.from_user.id} INN={inn} ga adminstartor emas...")
                await message.answer(f"{message.document.file_name} sizga tegishli emas...")
                await bot.send_message(superuser, f"{message.document.file_name} {message.from_user.id} ga tegishli emas")
        except Exception as e:
            await message.answer("Fayl qabul qilinmadi.")
            await bot.send_message(superuser, f"{message.from_user.id}: {e} bu otchet emas")

async def scan_photo(message: types.file):
    try:
        file_info = await bot.get_file(message.photo[-1].file_id)
        downloaded_file = await bot.download_file(file_info.file_path)
        file_name,file_extension = os.path.splitext(file_info.file_path)

        fnam = file_name.split('/')
        filename = fnam[-1]
        path_sep = os.path.sep
        fil = rootpath() + path_sep + 'photos' + path_sep
        src = fil + filename + file_extension

        if message.from_user.id == superuser:  # superUser
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file.getvalue())
            logger.info(f"{superuser} SuperUser saved as {src}")
            await message.answer(f"{src}\nholatda SuperUser tomonidan saqlab qo'yildi.")
        else:
           logger.info(f"fayli qabul qilinmadi.")
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
async def dirinn(message: types.Message):
    user_id = message.from_user.id
    inn = message.text[6:]
    if (inn.strip()==''):
        await message.answer("Komanda noto'g'ri berildi.  (INN ko'rsatilmadi.)")
    else:
        logger.info(f"\n{message.from_user.id} /dirx natijasi")
        path_sep = os.path.sep
        fil = rootpath() + path_sep + 'files' + path_sep
        f1 = f"<b>{inn} hisobotlari.</b>\n"
        f2 = f1
        for root, dirs, files in os.walk(fil):
            for filename in files:
                innf = filename[0:9]
                #print(f"{inn=}-{innf=}")
                if inn==innf:
                    src = fil + filename
                    f1 = f1 + filename + '\n'
                    f2 = f2 + src + '\n'
        await message.answer(f1)
        logger.info(f"\n{f2}")

async def my(message: Message):
    # //TODO  my
    inns = await con.get_rek(message.from_user.id)
    n = len(inns)
    s = '<b>Mening tashkilotlarim.</b>\n'
    for i in range(n):
        nam = await con.inn_rek(inns[i][0])
        s = s + f"{inns[i][0]} {nam[0]}" +'\n'
    logger.info(f"{message.from_user.id}/my results\n{s}")
    await message.answer(s)

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
    if message.from_user.id == superuser:  # superUser
        logger.info(f"\n{message.from_user.id} /copy natijasi")
        path_sep = os.path.sep
        fil = rootpath() + path_sep + 'files' + path_sep
        i = 0
        for root, dirs, files in os.walk(fil):
            for filename in files:
                src = fil + filename
                doc = open(src, 'rb')
                await message.reply_document(doc)
                i = i + 1
                logger.info(f"{i} getted file {src}")
                #print(date_time,i, 'Получен файл', src)
async def copybase(message: types.Message):
    file1 = 'dbase_sqlite.db'
    if message.from_user.id == superuser:  # superUser
        logger.info(f"\n{message.from_user.id} /copybase natijasi")
        path_sep = os.path.sep
        fil = rootpath() + path_sep + 'files' + path_sep
        fil1 = rootpath() + path_sep

        src = fil1 + file1
        doc = open(src, 'rb')
        await message.reply_document(doc)
        logger.info(f"getted file {src}")

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
'''
async def drop_org(message: types.Message):
    if message.from_user.id == superuser:  # superUser
        logger.info(f"\n{message.from_user.id} /droporg natijasi")
        #now = datetime.now()  # current date and time
        #date_time = now.strftime("%Y.%m.%d %H:%M:%S") + ':'
        await con.droporg()
        await message.answer('dropped table ORG ...')
        #print(date_time,'dropping table ORG ...')
        logger.info(f"dropped table ORG ...")

async def dropadm(message: types.Message):
    if message.from_user.id == superuser:  # superUser
        logger.info(f"\n{message.from_user.id} /dropadm natijasi")
        await con.dropadm()
        await message.answer('dropped table ADMIN ...')
        logger.info(f"{message.from_user.id} dropped table ADMIN ...")
'''
def register_admin(dp: Dispatcher):
    dp.register_message_handler(adm_reg, commands=["addadmin"], state="*", is_admin=True)
    dp.register_message_handler(adm_del, commands=["deladmin"], state="*", is_admin=True)
    dp.register_message_handler(adm_info, commands=["admins"], state="*", is_admin=True)
    dp.register_message_handler(user_reg, commands=["reg"], state="*", is_admin=True)
    dp.register_message_handler(clients, commands=["users"], state="*", is_admin=True)
    dp.register_message_handler(send_inn, commands=["addinn"], state="*", is_admin=True)
    dp.register_message_handler(del_inn, commands=["delinn"], state="*", is_admin=True)
    dp.register_message_handler(info_inn, commands=["inns"], state="*", is_admin=True)
    dp.register_message_handler(send_adm, commands=["sendadm"], state="*", is_admin=True)
    dp.register_message_handler(send_all, commands=["sendall"], state="*", is_admin=True)
    dp.register_message_handler(scan_doc, content_types=[types.ContentType.DOCUMENT], is_admin=True)
    dp.register_message_handler(scan_photo,content_types=[types.ContentType.PHOTO], is_admin=True)
    dp.register_message_handler(dirfiles, commands=["dir"], state="*", is_admin=True)
    dp.register_message_handler(dirinn, commands=["dirx"], state="*", is_admin=True)
    dp.register_message_handler(my, commands=["my"], state="*", is_admin=True)
    dp.register_message_handler(deletefile, commands=["del"], state="*", is_admin=True)
    dp.register_message_handler(copydoc, commands=["copy"], state="*", is_admin=True)
    dp.register_message_handler(copybase, commands=["copybase"], state="*", is_admin=True)
    dp.register_message_handler(copylogfile, commands=["copylog"], state="*", is_admin=True)
    dp.register_message_handler(droplogfile, commands=["droplog"], state="*", is_admin=True)
#    dp.register_message_handler(drop_org, commands=["droporg"], state="*", is_admin=True)
#    dp.register_message_handler(dropadm, commands=["dropadm"], state="*", is_admin=True)
