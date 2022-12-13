import xlrd,os

async def readxls(filexls,nomertel):
    ''' читаем .xls файла с помощью xlrd для чтение .xlsx  openpyxl.
        находим данные из файла по номеру телефона
     '''

    sss =''

    try:
        book = xlrd.open_workbook(filexls)
        sheet = book.sheet_by_index(0)
        row = sheet.nrows
        col = sheet.ncols

        nomercol = 0

        tel = ''
        nomertel1 =  str(int(nomertel))

        for m in range(row):
            tel = sheet.cell_value(m,0)
            if (tel==nomertel or tel==nomertel1):
                nomercol=m
                break

        frm = 25

        if nomercol > 0:
            for i in range(1,col):
                if (i>9):
                    sh = sheet.cell_value(2,i)[0:frm].ljust(frm,'.')
                    dn = sheet.cell_value(nomercol,i)
                    if (dn != 0.0):
                        sss = sss +  sh+' '+"{:9.2f}".format(dn).strip() +'\n'
                else:
                    sh = sheet.cell_value(2,i).strip()
                    dn = sheet.cell_value(nomercol,i)
                    if (type(dn)==float):
                        dn = str(int(dn))
                    sss = sss + sh+' '+ dn +'\n'
        else:
            sss =''
            print(nomertel + ' nomeri ' + filexls +' da faylida topilmadi')

    except FileNotFoundError as err:
        sss = "Bu oy ma'lumotlari serverga joylashtirilmagan !"
        print(f"{err}")

    if sss=='':
        sss = "Ma'lumot topilmadi..."+"\n"

    return sss
    
#-----------------------------------------------
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
