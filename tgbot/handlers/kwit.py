import xlrd
from create_bot import con,logger
from datetime import datetime

async def readxls(filexls, nomertel,inn):
    ''' читаем .xls файла с помощью xlrd для чтение .xlsx  openpyxl.
        находим данные из файла по номеру телефона
     '''
    mess = ''
    sss = ''
    #now = datetime.now()  # current date and time
    #date_time = now.strftime("%Y.%m.%d %H:%M:%S") + ':'

    rek = await con.inn_rek(inn)
    if not None:
        sss = str(inn)+':' + rek[0]
        logger.info(f"{sss}")
        sss = sss + '\n'
    try:
        book = xlrd.open_workbook(filexls)
        sheet = book.sheet_by_index(0)
        row = sheet.nrows
        col = sheet.ncols

        nomercol = 0

        nomertel1 = str(int(nomertel))

        for m in range(row):
            tel = ''.join(str(sheet.cell_value(m, 0)).strip().split(' '))
            if (nomertel==tel  or nomertel1==tel):
                logger.info(f"{nomertel} {sheet.cell_value(m, 0)}")
                nomercol = m
                break
        frm = 18
        if nomercol > 0:
            for i in range(1, col):
                if (i > 9):
                    sh = sheet.cell_value(2, i)[0:frm].ljust(frm, '.')
                    dn = sheet.cell_value(nomercol, i)

                    #print(i,sh,dn)
                    if (dn != 0.0):
                        #print(i,sh,dn,type(dn))
                        sss = sss + sh + ' ' + "{:9.2f}".format(dn).strip().rjust(11) + '\n'
                else:
                    if i==9:
                        sss = sss + '\n'
                        mess = sheet.cell_value(nomercol, i)
                    else:
                        sh = sheet.cell_value(2, i).strip()
                        dn = sheet.cell_value(nomercol, i)
                        #print(i, sh, dn)
                        if (type(dn) == float):
                            dn = str(int(dn))
                        sss = sss + sh + ' ' + dn + '\n'
            if mess!='':
                try:
                    int(mess)
                except:
                    sss = mess +'\n\n' + sss
        else:
            sss = ''
            #print(date_time,nomertel + ' nomeri ' + filexls + ' da faylida topilmadi')

    except FileNotFoundError as err:
        sss = "Bu oy ma'lumotlari serverga joylashtirilmagan !"

        logger.info(f"{err}")
        logger.info(f"{filexls} fayli topilmadi")

    if sss == '':
        sss = f"{nomertel} bo'yicha ma'lumot topilmadi...\n"
        logger.info(f"{nomertel} nomeri {filexls} da faylida topilmadi")

    return '<code>'+ sss +  '</code>'

#<code>inline fixed-width code</code>

# -----------------------------------------------
'''
import os
def main():
    os.system('cls')
    sss = readxls(r'.\files\2022_10.xls','+998905701021')
    await print(sss)

#---------------------------------
if __name__ == '__main__':
    main()     
'''
