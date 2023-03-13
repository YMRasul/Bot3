import xlrd
from create_bot import con,logger
async def readxls(mes,filexls, nomertel,inn):
    ''' читаем .xls файла с помощью xlrd для чтение .xlsx  openpyxl.
        находим данные из файла по номеру телефона
     '''
    kol = []
    msg = []

    ret = []
    ret.append(0)
    try:
        book = xlrd.open_workbook(filexls)
        sheet = book.sheet_by_index(0)
        row = sheet.nrows
        col = sheet.ncols

        nomertel1 = str(int(nomertel))
        for m in range(row):
            tel = ''.join(str(sheet.cell_value(m, 0)).strip().split(' '))
            if (nomertel==tel  or nomertel1==tel):
                #logger.info(f"{nomertel} {sheet.cell_value(m, 0)}")
                kol.append(m)
        frm = 18
        if len(kol) > 0:
            ret[0] = 1
            for nomercol in kol:
                mess = ''
                sss = ''
                rek = await con.inn_rek(inn)
                #print(f"{rek=}")
                if rek:
                    sss = str(inn) + ':' + rek[0]
                    #logger.info(f"{sss}")
                    sss = sss + '\n'
                for i in range(1, col):
                    if (i > 9):
                        sh = sheet.cell_value(2, i)[0:frm].ljust(frm, '.')
                        dn = sheet.cell_value(nomercol, i)
                        if (dn != 0.0):
                            sss = sss + sh + ' ' + format(dn,"11,.2f").strip().rjust(14) + '\n'
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
                msg.append(sss)
            ret.append(msg)
        else:
            sss = f"{mes} ma'lumotida  {nomertel} nomeri topilmadi...\n"
            msg.append(sss)
            ret.append(msg)

    except FileNotFoundError as err:
        sss = f"{mes} uchun ma'lumot topilmadi"
        msg.append(sss)
        ret.append(msg)
        logger.info(f"{err}")
        logger.info(f"{filexls} fayli topilmadi")
    return ret
